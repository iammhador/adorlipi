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
        self.phonetic_parser = PhoneticParser(os.path.join(data_dir, 'mapping.json'))
        self.loanword_transliterator = EnglishLoanwordTransliterator(
            os.path.join(data_dir, 'loanwords.json'),
            self.phonetic_parser
        )
        self.suffix_handler = SuffixHandler()
        self.suggester = Suggester(os.path.join(data_dir, 'openbangla_dictionary.json'))
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
            return user_match

        if norm_text != text:
            user_match = self.user_dictionary.lookup(norm_text)
            if user_match:
                return user_match

        dict_match = self.dictionary.exact_lookup(text)
        if dict_match:
            return dict_match

        if norm_text != text:
            dict_match = self.dictionary.exact_lookup(norm_text)
            if dict_match:
                return dict_match

        return None

    def _root_lookup(self, root):
        match = self._exact_lookup(root)
        if match:
            return match, "dictionary_root"

        norm_root = self.normalizer.normalize(root)
        match = self.loanword_transliterator.transliterate(norm_root)
        if match:
            return match, "loanword_root"

        return None, None

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
            return None, None

        root, suffix = word.rsplit("-", 1)
        suffix = suffix.lower()
        root_bn, source = self._root_lookup(root)
        if not root_bn:
            return None, None

        joined = self._join_suffix(root_bn, suffix)
        if not joined:
            return None, None

        return joined, "compound_suffix_" + source

    def _plain_suffix_lookup(self, norm_word):
        root, suffix_bn = self.suffix_handler.strip_suffix(norm_word)
        if not suffix_bn:
            return None, None

        root_bn, source = self._root_lookup(root)
        if not root_bn:
            return None, None

        return root_bn + suffix_bn, "suffix_" + source

    def _pattern_lookup(self, norm_word):
        for pat in self.patterns:
            if re.search(pat['regex'], norm_word):
                return re.sub(pat['regex'], pat['replace'], norm_word)
        return None

    def _transliterate_word(self, token):
        norm_word = self.normalizer.normalize(token)

        exact_match = self._exact_lookup(token)
        if exact_match:
            return exact_match, "dictionary"

        compound_match, compound_source = self._compound_suffix_lookup(token)
        if compound_match:
            return compound_match, compound_source

        dict_match = self.dictionary.skeleton_lookup(norm_word)
        if dict_match:
            return dict_match, "skeleton_dictionary"

        loanword_match = self.loanword_transliterator.transliterate(norm_word)
        if loanword_match:
            return loanword_match, "loanword"

        suffix_match, suffix_source = self._plain_suffix_lookup(norm_word)
        if suffix_match:
            return suffix_match, suffix_source

        fuzzy_match = self.dictionary.fuzzy_lookup(norm_word)
        if fuzzy_match:
            return fuzzy_match, "fuzzy_dictionary"

        pattern_match = self._pattern_lookup(norm_word)
        if pattern_match:
            return pattern_match, "pattern"

        return self.phonetic_parser.parse(norm_word), "phonetic"

    def explain_word(self, word):
        output, source = self._transliterate_word(word)
        return {
            "input": word,
            "current_output": output,
            "source_layer": source,
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
                    candidates.append((match, idx + 1))

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
        Full pipeline: Exact Dict -> Pre-Process -> Tokenize -> Phrase Dict -> Normalize -> Dict -> Compound Suffix -> Loanword -> Suffix -> Patterns -> Phonetic -> Join
        """
        exact_match = self._exact_lookup(text)
        if exact_match:
            return exact_match

        text = self._pre_process(text)
        exact_match = self._exact_lookup(text)
        if exact_match:
            return exact_match

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

                parsed, _source = self._transliterate_word(token)
                result.append(parsed)
            else:
                result.append(self.phonetic_parser.parse(token))

            i += 1
                
        return "".join(result)
