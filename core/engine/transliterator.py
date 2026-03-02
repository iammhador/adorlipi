from .tokenizer import Tokenizer
from .normalizer import Normalizer
from .dictionary import Dictionary
from .phonetic_parser import PhoneticParser
from .suffix_handler import SuffixHandler
import os
import json
import re

class Transliterator:
    def __init__(self, data_dir=None):
        if data_dir is None:
            # Default to ../../data relative to this file (core/engine/ -> root/data/)
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            data_dir = os.path.join(base_dir, 'data')
            
        self.tokenizer = Tokenizer()
        self.normalizer = Normalizer()
        self.dictionary = Dictionary(os.path.join(data_dir, 'dictionary.json'))
        self.phonetic_parser = PhoneticParser(os.path.join(data_dir, 'mapping.json'))
        self.suffix_handler = SuffixHandler()
        
        # Load Patterns (Regex-based Fallback Heuristics)
        self.patterns = []
        try:
            with open(os.path.join(data_dir, 'patterns.json'), 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.patterns = data.get("patterns", [])
        except FileNotFoundError:
            pass

    def _pre_process(self, text):
        """
        Instantly merge common space-separated suffixes 
        (e.g., 'mon e' -> 'mone', 'kajta k' -> 'kajtak')
        before tokenizer splits them.
        """
        suffixes = ['e', 'er', 'te', 'k', 'ke', 're', 'der']
        for suf in suffixes:
            # Match word chars, followed by space(s), followed by suffix, 
            # and MUST be followed by space, punctuation or end of string.
            pattern = r'(?<=[a-zA-Z])\s+(' + re.escape(suf) + r')(?=[\s\.,!\?]|$)'
            text = re.sub(pattern, r'\1', text)
        return text

    def transliterate(self, text):
        """
        Full pipeline: Pre-Process -> Tokenize -> Normalize -> Dict -> Suffix+Dict -> Patterns -> Phonetic -> Join
        """
        text = self._pre_process(text)
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
                    # 3. Smart Suffix Handling
                    root, suffix_bn = self.suffix_handler.strip_suffix(norm_word)
                    if suffix_bn:
                        root_match = self.dictionary.lookup(root)
                        if root_match:
                            result.append(root_match + suffix_bn)
                            continue
                    
                    # 4. Pattern Matching (Regex Heuristics)
                    pattern_matched = False
                    for pat in self.patterns:
                        if re.search(pat['regex'], norm_word):
                            # Replace matching section
                            parsed = re.sub(pat['regex'], pat['replace'], norm_word)
                            # Transliterate the rest (if any) phonetically
                            # This is simple for full word matches (^pattern$). 
                            # If it's partial, we'd need more complex substitution. 
                            # Given our patterns are strictly ^word$ based for now, direct substitution is fine.
                            result.append(parsed)
                            pattern_matched = True
                            break
                    
                    if pattern_matched:
                        continue
                            
                    # 5. Phonetic Parsing (Fallback)
                    parsed = self.phonetic_parser.parse(norm_word)
                    result.append(parsed)
            else:
                result.append(self.phonetic_parser.parse(token))
                
        return "".join(result)
