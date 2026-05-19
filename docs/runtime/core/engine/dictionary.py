import json
import os
import difflib

class Dictionary:
    def __init__(self, data_path):
        self.data_path = data_path
        self.skeleton_index = {}
        self.max_phrase_words = 1
        self.dictionary = self._load_dictionary()
        self._keys = list(self.dictionary.keys())

    def _load_dictionary(self):
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.max_phrase_words = max([len(key.split()) for key in data if " " in key] or [1])
                self._build_skeletons(data)
                return data
        except FileNotFoundError:
            print(f"Warning: Dictionary file not found at {self.data_path}")
            return {}

    def _to_skeleton(self, word):
        """Strips vowels (except the first letter) to create a consonant skeleton."""
        if not word: 
            return word
        sk = word[0] + ''.join([c for c in word[1:] if c not in 'aeiouO'])
        return sk

    def _build_skeletons(self, data):
        """Build an index of skeleton keys pointing to the most likely full word."""
        for key in data.keys():
            # Skip very short words for skeletons to prevent aggressive mis-mapping
            if len(key) <= 3:
                continue
            sk = self._to_skeleton(key)
            # Store shortest original word for a skeleton
            if sk not in self.skeleton_index or len(key) < len(self.skeleton_index[sk]):
                self.skeleton_index[sk] = key

    def exact_lookup(self, word):
        """Strict dictionary lookup for rigid suffix/prefix processing."""
        if word in self.dictionary:
            return self.dictionary[word]
        return self.dictionary.get(word.lower())

    def skeleton_lookup(self, word):
        info = self.skeleton_lookup_with_meta(word)
        return info["text"] if info else None

    def skeleton_lookup_with_meta(self, word):
        word = word.lower()
        if len(word) >= 3:
            sk = self._to_skeleton(word)
            if sk == word and sk in self.skeleton_index:
                real_word = self.skeleton_index[sk]
                return {
                    "text": self.dictionary[real_word],
                    "matched_key": real_word,
                }
        return None

    def fuzzy_lookup(self, word):
        info = self.fuzzy_lookup_with_meta(word)
        return info["text"] if info else None

    def fuzzy_lookup_with_meta(self, word, cutoff=0.85):
        word = word.lower()
        if len(word) >= 4:
            matches = difflib.get_close_matches(word, self._keys, n=1, cutoff=cutoff)
            if matches:
                matched = matches[0]
                similarity = difflib.SequenceMatcher(None, word, matched).ratio()
                return {
                    "text": self.dictionary[matched],
                    "matched_key": matched,
                    "similarity": similarity,
                }
        return None

    def lookup(self, word):
        """
        Legacy layered dictionary lookup: Exact, Skeleton, Fuzzy
        """
        word = word.lower()
        res = self.exact_lookup(word)
        if res: return res
        
        res = self.skeleton_lookup(word)
        if res: return res
        
        return self.fuzzy_lookup(word)
