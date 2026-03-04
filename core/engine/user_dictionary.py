import os
import json

class UserDictionary:
    def __init__(self):
        # Store user dictionary in their local config directory
        config_dir = os.path.expanduser('~/.config/adorlipi')
        if not os.path.exists(config_dir):
            try:
                os.makedirs(config_dir)
            except Exception:
                pass
        
        self.data_path = os.path.join(config_dir, 'user_dict.json')
        self.dictionary = self._load()

    def _load(self):
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def _save(self):
        try:
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(self.dictionary, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Warning: Failed to save user dictionary: {e}")

    def learn(self, english_word, bangla_word):
        """
        Saves a user's manual selection to permanently override default behavior.
        """
        if not english_word or not bangla_word:
            return
            
        english_word = english_word.lower().strip()
        bangla_word = bangla_word.strip()
        
        # Don't save if it's already the primary mapping
        if self.dictionary.get(english_word) == bangla_word:
            return
            
        self.dictionary[english_word] = bangla_word
        self._save()

    def lookup(self, english_word):
        """
        Returns the user's previously preferred Bangla word for this Keystroke.
        """
        if not english_word:
            return None
        return self.dictionary.get(english_word.lower().strip())
