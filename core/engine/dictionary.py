import json
import os

class Dictionary:
    def __init__(self, data_path):
        self.data_path = data_path
        self.dictionary = self._load_dictionary()

    def _load_dictionary(self):
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Dictionary file not found at {self.data_path}")
            return {}

    def lookup(self, word):
        """
        Returns the Bangla replacement if found, else None.
        Case insensitive lookup.
        """
        return self.dictionary.get(word.lower()) 
