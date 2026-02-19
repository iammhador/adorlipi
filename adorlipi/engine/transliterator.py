from .tokenizer import Tokenizer
from .normalizer import Normalizer
from .dictionary import Dictionary
from .phonetic_parser import PhoneticParser
from .suffix_handler import SuffixHandler
import os

class Transliterator:
    def __init__(self, data_dir=None):
        if data_dir is None:
            # Default to ../data relative to this file
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_dir, 'data')
            
        self.tokenizer = Tokenizer()
        self.normalizer = Normalizer()
        self.dictionary = Dictionary(os.path.join(data_dir, 'dictionary.json'))
        self.phonetic_parser = PhoneticParser(os.path.join(data_dir, 'mapping.json'))
        self.suffix_handler = SuffixHandler()

    def transliterate(self, text):
        """
        Full pipeline: Tokenize -> Normalize -> Dict -> Suffix+Dict -> Phonetic -> Join
        """
        tokens = self.tokenizer.tokenize(text)
        result = []
        
        for token in tokens:
            if self.tokenizer.is_word(token):
                # 1. Normalize
                norm_word = self.normalizer.normalize(token)
                
                # 2. Dictionary Lookup (Full Word)
                dict_match = self.dictionary.lookup(norm_word)
                if dict_match:
                    result.append(dict_match)
                else:
                    # 3. Smart Suffix Handling (New)
                    root, suffix_bn = self.suffix_handler.strip_suffix(norm_word)
                    if suffix_bn:
                        # Check if root exists in dictionary
                        root_match = self.dictionary.lookup(root)
                        if root_match:
                            # Combine: Dictionary Root + Suffix
                            # This handles 'manus' (মানুষ) + 'er' (ের) -> মানুষের
                            result.append(root_match + suffix_bn)
                            continue
                            
                    # 4. Phonetic Parsing (Fallback)
                    parsed = self.phonetic_parser.parse(norm_word)
                    result.append(parsed)
            else:
                # Punctuation/Whitespace: Parse it too in case of mapping (., 1, etc)
                # Whitespace will pass through if not mapped.
                result.append(self.phonetic_parser.parse(token))
                
        return "".join(result)
