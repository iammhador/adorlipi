class SuffixHandler:
    def __init__(self):
        # Suffixes sorted by length (longest first) to ensure greedy matching
        # e.g. check 'gulo' before 'o' (if we had 'o')
        self.suffixes = [
            ("gulo", "গুলো"),
            ("gula", "গুলা"),
            ("gulo", "গুলো"),
            ("der", "দের"),
            ("ra", "রা"),
            ("ta", "টা"),
            ("ti", "টি"),
            ("te", "তে"),
            ("ke", "কে"),
            ("er", "ের"),
            # ("r", "র"), # 'r' is too common/ambiguous for simplistic stripping? 
            # e.g. 'bar' -> 'ba'+'r'? 'katar' -> 'kata'+'r'? 
            # 'amar' is in dict. 
            # Let's check 'er' first, usually 'er' is the possessive suffix.
        ]

    def strip_suffix(self, word):
        """
         Checks if word ends with a known suffix.
         Returns (root, bangla_suffix) if found, else (word, None).
        """
        # Iterate through suffixes
        for suffix_en, suffix_bn in self.suffixes:
            if word.endswith(suffix_en):
                # Ensure the root is at least 2 chars long to avoid over-stripping short words
                # e.g. 'her' -> 'h'+'er'? 'ter'?
                if len(word) > len(suffix_en) + 1:
                    root = word[:-len(suffix_en)]
                    return root, suffix_bn
        
        return word, None
