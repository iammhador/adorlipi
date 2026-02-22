import re

class Normalizer:
    def __init__(self):
        # Characters that have case-sensitive mappings in mapping.json
        # N=ণ, NG=ঙ, NGV=ঞ, J=য — must be preserved
        self.case_sensitive_chars = {'N', 'J'}
        self.case_sensitive_combos = {'NG', 'NGV'}
        
        self.replacements = [
            (r'ph', 'f'),
            (r'tmi', 'tumi'),
        ]
        
    def normalize(self, word):
        """
        Normalizes a word: smart lowercasing (preserving N/J/NG), 
        removing excessive repeats, and applying substitutions.
        """
        # 1. Smart lowercase: preserve N, J, NG, NGV
        # Replace case-sensitive combos with placeholders first
        preserved = word
        preserved = preserved.replace('NGV', '\x01NGV\x01')
        preserved = preserved.replace('NG', '\x01NG\x01')
        
        # Now process character by character
        result = []
        i = 0
        while i < len(preserved):
            if preserved[i] == '\x01':
                # Extract preserved combo
                end = preserved.index('\x01', i + 1)
                result.append(preserved[i+1:end])
                i = end + 1
            elif preserved[i] in self.case_sensitive_chars:
                result.append(preserved[i])
                i += 1
            else:
                result.append(preserved[i].lower())
                i += 1
        
        word = ''.join(result)
        
        # 2. Remove repeated characters (more than 2) -> reduce to 1
        word = re.sub(r'(.)\1{2,}', r'\1', word)
        
        # 3. Apply specific replacements
        for pattern, replacement in self.replacements:
            word = re.sub(pattern, replacement, word)

        return word
