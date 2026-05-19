import json
import os
import re


class EnglishLoanwordTransliterator:
    def __init__(self, data_path=None, phonetic_parser=None):
        if data_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            data_path = os.path.join(base_dir, 'data', 'loanwords.json')

        self.data_path = data_path
        self.phonetic_parser = phonetic_parser
        self.loanwords = self._load()
        self.triggers = [
            'tion', 'sion', 'ment', 'ance', 'ence', 'qu', 'ck', 'igh', 'ph'
        ]

    def _load(self):
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def lookup(self, word):
        if not word:
            return None
        return self.loanwords.get(word.lower())

    def transliterate(self, word):
        info = self.transliterate_with_meta(word)
        return info["text"] if info else None

    def transliterate_with_meta(self, word):
        if not word or not re.fullmatch(r"[A-Za-z]+", word):
            return None

        key = word.lower()
        direct = self.lookup(key)
        if direct:
            return {
                "text": direct,
                "is_direct": True,
                "matched_key": key,
                "rewritten": key,
            }

        if not self._looks_like_english(key):
            return None

        rewritten = self._rewrite_to_banglish(key)
        if not rewritten or rewritten == key or not self.phonetic_parser:
            return None

        return {
            "text": self.phonetic_parser.parse(rewritten),
            "is_direct": False,
            "matched_key": None,
            "rewritten": rewritten,
        }

    def _looks_like_english(self, word):
        if len(word) < 5:
            return False
        if self.has_strong_english_signal(word):
            return True
        return bool(re.search(r"(?:er|or|le|ive|ed|y)$", word))

    def has_strong_english_signal(self, word):
        if not word:
            return False
        return any(trigger in word for trigger in self.triggers)

    def _rewrite_to_banglish(self, word):
        replacements = [
            (r"tion$", "shon"),
            (r"sion$", "shon"),
            (r"ment$", "ment"),
            (r"ance$", "ans"),
            (r"ence$", "ens"),
            (r"igh", "ai"),
            (r"qu", "ku"),
            (r"ck", "k"),
            (r"ph", "f"),
            (r"oo", "u"),
            (r"ee", "i"),
            (r"ea", "i"),
            (r"ai", "ei"),
            (r"ay$", "e"),
            (r"c(?=[eiy])", "s"),
            (r"c", "k"),
            (r"g(?=[eiy])", "j"),
        ]

        rewritten = word
        if len(rewritten) > 4 and rewritten.endswith("e") and not rewritten.endswith(("ee", "le")):
            rewritten = rewritten[:-1]

        for pattern, repl in replacements:
            rewritten = re.sub(pattern, repl, rewritten)

        return rewritten
