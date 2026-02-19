
import unittest
from adorlipi.engine.normalizer import Normalizer
from adorlipi.engine.transliterator import Transliterator

class TestRefinements(unittest.TestCase):
    def setUp(self):
        self.norm = Normalizer()
        self.trans = Transliterator()

    def test_aa_preservation(self):
        # Normalizer should NOT collapse 'aa' if we want 'aa' -> 'আ'
        # normalized = self.norm.normalize("aam")
        # self.assertEqual(normalized, "aam") 
        
        # Mapping check
        # 'aa' -> 'আ', 'm' -> 'ম' => 'আম'
        res = self.trans.transliterate("aam")
        print(f"DEBUG: aam -> {res}")
        self.assertEqual(res, "আম")

    def test_pera_somossa(self):
        # These likely need dictionary entries or corrected mappings
        # somosssa -> সমস্যা
        res = self.trans.transliterate("somosssa")
        print(f"DEBUG: somosssa -> {res}")
        # Note: 'somosssa' is a bit weird input, likely means 'somossa'
        
        # pera -> প্যারা (slang)
        res = self.trans.transliterate("pera")
        print(f"DEBUG: pera -> {res}")
        
        # Test somossa
        res = self.trans.transliterate("somossa")
        print(f"DEBUG: somossa -> {res}")

if __name__ == '__main__':
    unittest.main()
