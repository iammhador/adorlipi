class SuffixHandler:
    def __init__(self):
        # Suffixes sorted by length (longest first) to ensure greedy matching
        # e.g. check 'gulo' before 'o' (if we had 'o')
        self.suffixes = [
            ("techhilam", "তেছিলাম"),
            ("techhilen", "তেছিলেন"),
            ("techhish", "তেছিস"),
            ("techhen", "তেছেন"),
            ("chhilen", "ছিলেন"),
            ("chhilam", "ছিলাম"),
            ("techhe", "তেছে"),
            ("chhish", "ছিস"),
            ("chhen", "ছেন"),
            ("echhi", "েছি"),
            ("echho", "েছো"),
            ("echhe", "েছে"),
            ("echen", "েছেন"),
            ("gulo", "গুলো"),
            ("gula", "গুলা"),
            ("chhilo", "ছিলো"),
            ("tuku", "টুকু"),
            ("der", "দের"),
            ("dero", "দেরও"),
            ("tai", "টাই"),
            ("tei", "তেই"),
            ("rao", "রাও"),
            ("lam", "লাম"),
            ("len", "লেন"),
            ("tem", "তেম"),
            ("ten", "তেন"),
            ("ra", "রা"),
            ("ta", "টা"),
            ("ti", "টি"),
            ("te", "তে"),
            ("ke", "কে"),
            ("er", "ের"),
            ("e", "ে"),
            ("o", "ও")
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
