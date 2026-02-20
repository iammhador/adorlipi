import re

class Tokenizer:
    def __init__(self):
        # Pattern to capture words and punctuation separately
        # \w+ matches words (alphanumeric)
        # [^\w\s]+ matches punctuation
        # \s+ matches whitespace
        self.pattern = re.compile(r"(\w+|[^\w\s]+|\s+)")

    def tokenize(self, text):
        """
        Splits text into a list of tokens (words, punctuation, whitespace).
        """
        return re.findall(r'\w+|[^\w\s]+|\s+', text)

    def is_word(self, token):
        """
        Checks if a token is a word (alphanumeric).
        """
        return token.isalnum()
