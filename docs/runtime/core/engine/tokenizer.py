import re

class Tokenizer:
    def __init__(self):
        # Pattern to capture words and punctuation separately
        # ASCII compounds keep dictionary keys like "ami-i" and "kalo_jam" intact.
        # [^\w\s]+ matches punctuation
        # \s+ matches whitespace
        self.pattern = re.compile(r"([A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)*|\w+|[^\w\s]+|\s+)")
        self.compound_word_pattern = re.compile(r"[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)+")

    def tokenize(self, text):
        """
        Splits text into a list of tokens (words, punctuation, whitespace).
        """
        return self.pattern.findall(text)

    def is_word(self, token):
        """
        Checks if a token is a word (alphanumeric).
        """
        return token.isalnum() or bool(self.compound_word_pattern.fullmatch(token))
