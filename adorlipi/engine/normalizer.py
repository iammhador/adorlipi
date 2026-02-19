import re

class Normalizer:
    def __init__(self):
        self.replacements = [
            (r'^v', 'bh'),  # Start v -> bh (rules based)
            (r'ph', 'f'),
            (r'sh', 'sh'), # explicit keep
            (r'ss', 'sh'),
            (r'aa', 'a'),  # collapse aa -> a
            (r'tmi', 'tumi'),
            (r'r', 'r'),
        ]
        
    def normalize(self, word):
        """
        Normalizes a word by lowercasing, removing repeats, and applying substitutions.
        """
        word = word.lower()
        
        # 1. Remove repeated characters (more than 2) -> reduce to 1
        # e.g., 'bhaaaai' -> 'bhai', 'khuuuub' -> 'khub'
        # Exception: 'ee' and 'oo' might be meaningful, but for MVP standardizing to single chars usually helps mapping
        # Let's use a regex to collapse 3+ same chars to 1
        word = re.sub(r'(.)\1{2,}', r'\1', word)
        
        # 2. General common mappings/corrections
        
        # Handle 'v' at start -> 'bh' often helpful for phonetic mapping
        # specific check if 'v' is acceptable as 'b' or 'bh'
        if word.startswith('v'):
             # Simplistic rule: replace leading v with bh for better mapping if pure phonetic
             # But 'vai' -> 'bhai' dict lookup handles common ones.
             # This is for unknown words provided we wanted 'v' -> 'bh'
             word = 'bh' + word[1:]

        
        # 3. Apply specific replacements
        for pattern, replacement in self.replacements:
             # Use regex sub for all to support boundaries if needed, or simple string replace if no regex chars
             # For MVP, assuming patterns are regex-safe or simple strings
             word = re.sub(pattern, replacement, word)

        return word
