from .tokenizer import Tokenizer
from .normalizer import Normalizer
from .dictionary import Dictionary
from .phonetic_parser import PhoneticParser
from .suffix_handler import SuffixHandler
from .suggester import Suggester
from .user_dictionary import UserDictionary
from .context_engine import ContextEngine
from .loanword_transliterator import EnglishLoanwordTransliterator
import os
import json
import re

class Transliterator:
    def __init__(self, data_dir=None):
        if data_dir is None:
            # Default to ../../data relative to this file (core/engine/ -> root/data/)
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            data_dir = os.path.join(base_dir, 'data')
            
        self.tokenizer = Tokenizer()
        self.normalizer = Normalizer()
        self.dictionary = Dictionary(os.path.join(data_dir, 'dictionary.json'))
        self.phonetic_parser = PhoneticParser(
            os.path.join(data_dir, 'mapping.json'),
            conjunct_map_path=os.path.join(data_dir, 'inspired_conjuncts.json'),
            overrides_path=os.path.join(data_dir, 'phonetic_overrides.json'),
        )
        self.loanword_transliterator = EnglishLoanwordTransliterator(
            os.path.join(data_dir, 'loanwords.json'),
            self.phonetic_parser
        )
        self.suffix_handler = SuffixHandler()
        self.suggester = Suggester(
            os.path.join(data_dir, 'openbangla_dictionary.json'),
            conversational_data_path=os.path.join(data_dir, 'dictionary.json'),
        )
        self.user_dictionary = UserDictionary()
        self.context_engine = ContextEngine()
        
        # Connect context engine to suggester for context-aware ranking
        self.suggester.set_context_engine(self.context_engine)
        
        # Load Patterns (Regex-based Fallback Heuristics)
        self.patterns = []
        try:
            with open(os.path.join(data_dir, 'patterns.json'), 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.patterns = data.get("patterns", [])
        except FileNotFoundError:
            pass

        self.banglish_inflection_suffixes = (
            "chhi", "chi", "silo", "lam", "len", "ben", "bo",
            "si", "ta", "ti", "ra", "er", "e", "r",
        )
        self.high_risk_ambiguity = self._load_high_risk_ambiguity(
            os.path.join(data_dir, "high_risk_ambiguity.json")
        )

    def _candidate(self, text, source, confidence=1.0, matched_key=None):
        return {
            "text": text,
            "source": source,
            "confidence": confidence,
            "matched_key": matched_key,
        }

    def _load_high_risk_ambiguity(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            return {}

        if not isinstance(data, dict):
            return {}

        normalized = {}
        for key, payload in data.items():
            if not isinstance(key, str):
                continue
            if not isinstance(payload, dict):
                continue
            family = payload.get("preferred_family", [])
            if not isinstance(family, list):
                continue
            family = [word for word in family if isinstance(word, str)]
            if family:
                normalized[key.lower()] = {"preferred_family": set(family)}
        return normalized

    def _pre_process(self, text):
        """
        Instantly merge common space-separated suffixes 
        (e.g., 'mon e' -> 'mone', 'kajta k' -> 'kajtak')
        before tokenizer splits them.
        """
        suffixes = ['e', 'er', 'te', 'k', 'ke', 're', 'der']
        for suf in suffixes:
            # Match word chars, followed by space(s), followed by suffix, 
            # and MUST be followed by space, punctuation or end of string.
            pattern = r'(?<=[a-zA-Z])\s+(' + re.escape(suf) + r')(?=[\s\.,!\?]|$)'
            text = re.sub(pattern, r'\1', text)
        return text

    def get_suggestions(self, buffer):
        """
        Returns a list of auto-complete suggestions based on the user's current buffer.
        """
        if not buffer:
            return []
        
        # Tokenize to isolate punctuation from the actual alphanumeric word
        tokens = self.tokenizer.tokenize(buffer)
        if not tokens:
            return []
            
        last_token = tokens[-1]
        
        # Do not autocomplete naked punctuation marks (e.g. typing '"')
        if not self.tokenizer.is_word(last_token):
            return []
            
        target_bangla = self.transliterate(last_token)
        return self.suggester.get_suggestions(last_token, target_bangla)

    def learn(self, english_word, bangla_word):
        """
        Teaches the engine a user's preferred transliteration.
        Called when user manually selects a non-default candidate.
        """
        self.user_dictionary.learn(english_word, bangla_word)

    def _exact_lookup(self, text):
        norm_text = self.normalizer.normalize(text)

        user_match = self.user_dictionary.lookup(text)
        if user_match:
            return self._candidate(user_match, "dictionary", confidence=1.0, matched_key=text.lower().strip())

        if norm_text != text:
            user_match = self.user_dictionary.lookup(norm_text)
            if user_match:
                return self._candidate(user_match, "dictionary", confidence=1.0, matched_key=norm_text)

        dict_match = self.dictionary.exact_lookup(text)
        if dict_match:
            return self._candidate(dict_match, "dictionary", confidence=1.0, matched_key=text.lower())

        if norm_text != text:
            dict_match = self.dictionary.exact_lookup(norm_text)
            if dict_match:
                return self._candidate(dict_match, "dictionary", confidence=1.0, matched_key=norm_text)

        return None

    def _root_lookup(self, root):
        match = self._exact_lookup(root)
        if match:
            return self._candidate(
                match["text"],
                "dictionary_root",
                confidence=match["confidence"],
                matched_key=match["matched_key"],
            )

        norm_root = self.normalizer.normalize(root)
        loanword = self._loanword_candidate(norm_root, source="loanword_root")
        if loanword:
            return loanword

        return None

    def _join_suffix(self, root_bn, suffix_en):
        suffixes = {
            "guloi": "গুলোই",
            "gulo": "গুলো",
            "gula": "গুলা",
            "der": "দের",
            "tao": "টাও",
            "tai": "টাই",
            "tei": "তেই",
            "rao": "রাও",
            "rai": "রাই",
            "ra": "রা",
            "ta": "টা",
            "ti": "টি",
            "te": "তে",
            "ke": "কে",
            "e": "ে",
            "o": "ও",
        }

        if suffix_en in ("r", "er"):
            if root_bn.endswith(("া", "আ")):
                return root_bn + "য়ের"
            return root_bn + "র" if suffix_en == "r" else root_bn + "ের"

        if suffix_en == "e" and root_bn.endswith(("া", "আ", "ং")):
            return root_bn + "য়ে"

        suffix_bn = suffixes.get(suffix_en)
        if suffix_bn:
            return root_bn + suffix_bn

        return None

    def _compound_suffix_lookup(self, word):
        if "-" not in word:
            return None

        root, suffix = word.rsplit("-", 1)
        suffix = suffix.lower()
        root_candidate = self._root_lookup(root)
        if not root_candidate:
            return None

        joined = self._join_suffix(root_candidate["text"], suffix)
        if not joined:
            return None

        return self._candidate(
            joined,
            "compound_suffix_" + root_candidate["source"],
            confidence=root_candidate["confidence"],
            matched_key=root_candidate["matched_key"],
        )

    def _plain_suffix_lookup(self, norm_word):
        root, suffix_bn = self.suffix_handler.strip_suffix(norm_word)
        if not suffix_bn:
            return None

        root_candidate = self._root_lookup(root)
        if not root_candidate:
            return None

        return self._candidate(
            root_candidate["text"] + suffix_bn,
            "suffix_" + root_candidate["source"],
            confidence=root_candidate["confidence"],
            matched_key=root_candidate["matched_key"],
        )

    def _pattern_lookup(self, norm_word):
        for pat in self.patterns:
            if re.search(pat['regex'], norm_word):
                replaced = re.sub(pat['regex'], pat['replace'], norm_word)
                return self._candidate(replaced, "pattern", confidence=0.65, matched_key=pat['regex'])
        return None

    def _looks_like_banglish_inflected_word(self, word):
        lower = word.lower()
        if len(lower) < 4:
            return False
        return any(lower.endswith(suffix) for suffix in self.banglish_inflection_suffixes)

    def _loanword_candidate(self, norm_word, source="loanword"):
        loanword = self.loanword_transliterator.transliterate_with_meta(norm_word)
        if not loanword:
            return None

        if loanword["is_direct"]:
            return self._candidate(
                loanword["text"],
                source,
                confidence=0.97,
                matched_key=loanword["matched_key"],
            )

        if not self.loanword_transliterator.has_strong_english_signal(norm_word):
            return None

        if self._looks_like_banglish_inflected_word(norm_word):
            return None

        return self._candidate(
            loanword["text"],
            source,
            confidence=0.78,
            matched_key=loanword["rewritten"],
        )

    def _fuzzy_candidate(self, norm_word, phonetic_candidate=None):
        fuzzy = self.dictionary.fuzzy_lookup_with_meta(norm_word, cutoff=0.85)
        if not fuzzy:
            return None

        matched_key = fuzzy["matched_key"]
        similarity = fuzzy.get("similarity", 0.0)

        if not matched_key or matched_key[0] != norm_word[0]:
            return None
        if abs(len(norm_word) - len(matched_key)) > 1:
            return None
        if similarity < 0.92:
            return None

        ambiguity = self.high_risk_ambiguity.get(norm_word)
        if ambiguity and phonetic_candidate:
            preferred_family = ambiguity.get("preferred_family", set())
            if (
                phonetic_candidate["text"] in preferred_family
                and fuzzy["text"] not in preferred_family
            ):
                return None

        return self._candidate(
            fuzzy["text"],
            "fuzzy_dictionary",
            confidence=similarity,
            matched_key=matched_key,
        )

    def _transliterate_word(self, token):
        norm_word = self.normalizer.normalize(token)
        phonetic_candidate = self._candidate(
            self.phonetic_parser.parse(norm_word),
            "phonetic",
            confidence=0.5,
            matched_key=norm_word,
        )

        exact_match = self._exact_lookup(token)
        if exact_match:
            return exact_match

        compound_match = self._compound_suffix_lookup(token)
        if compound_match:
            return compound_match

        suffix_match = self._plain_suffix_lookup(norm_word)
        if suffix_match:
            return suffix_match

        dict_match = self.dictionary.skeleton_lookup_with_meta(norm_word)
        if dict_match:
            return self._candidate(
                dict_match["text"],
                "skeleton_dictionary",
                confidence=0.88,
                matched_key=dict_match["matched_key"],
            )

        loanword_match = self._loanword_candidate(norm_word)
        if loanword_match:
            return loanword_match

        fuzzy_match = self._fuzzy_candidate(norm_word, phonetic_candidate=phonetic_candidate)
        if fuzzy_match:
            return fuzzy_match

        pattern_match = self._pattern_lookup(norm_word)
        if pattern_match:
            return pattern_match

        return phonetic_candidate

    def explain_word(self, word):
        candidate = self._transliterate_word(word)
        output = candidate["text"]
        source = candidate["source"]
        return {
            "input": word,
            "current_output": output,
            "source_layer": source,
            "confidence": candidate["confidence"],
            "matched_key": candidate["matched_key"],
            "dictionary_hit": source in {
                "dictionary",
                "skeleton_dictionary",
                "fuzzy_dictionary",
                "dictionary_root",
                "compound_suffix_dictionary_root",
                "suffix_dictionary_root",
            },
            "suspected_bad": source in {"phonetic", "fuzzy_dictionary"} and len(word) >= 5,
        }

    def _match_phrase(self, tokens, start):
        if self.dictionary.max_phrase_words <= 1:
            return None

        words = []
        candidates = []
        idx = start

        while idx < len(tokens) and len(words) < self.dictionary.max_phrase_words:
            token = tokens[idx]
            if not self.tokenizer.is_word(token):
                break

            words.append(token)
            if len(words) > 1:
                phrase = " ".join(words)
                match = self._exact_lookup(phrase)
                if match:
                    candidates.append((match["text"], idx + 1))

            next_idx = idx + 1
            if next_idx >= len(tokens):
                break

            separator = tokens[next_idx]
            if not separator.isspace() or "\n" in separator:
                break

            idx = next_idx + 1

        if candidates:
            return candidates[-1]

        return None

    def transliterate(self, text):
        """
        Full pipeline:
        Exact/User -> Pre-process -> Tokenize -> Phrase Dict -> Word Resolver
        (compound/plain suffix -> skeleton -> loanword(gated) -> fuzzy(gated) -> pattern -> phonetic)
        """
        exact_match = self._exact_lookup(text)
        if exact_match:
            return exact_match["text"]

        text = self._pre_process(text)
        exact_match = self._exact_lookup(text)
        if exact_match:
            return exact_match["text"]

        tokens = self.tokenizer.tokenize(text)
        result = []

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if self.tokenizer.is_word(token):
                phrase_match = self._match_phrase(tokens, i)
                if phrase_match:
                    phrase, next_i = phrase_match
                    result.append(phrase)
                    i = next_i
                    continue

                candidate = self._transliterate_word(token)
                result.append(candidate["text"])
            else:
                result.append(self.phonetic_parser.parse(token))

            i += 1
                
        return "".join(result)
