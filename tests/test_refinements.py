
import sys
import os
import unittest

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.engine.normalizer import Normalizer
from core.engine.transliterator import Transliterator

class TestRefinements(unittest.TestCase):
    def setUp(self):
        self.norm = Normalizer()
        self.trans = Transliterator()

    def test_aa_preservation(self):
        res = self.trans.transliterate("aam")
        print(f"DEBUG: aam -> {res}")
        self.assertEqual(res, "আম")

    def test_pera_somossa(self):
        res = self.trans.transliterate("somosssa")
        print(f"DEBUG: somosssa -> {res}")
        
        res = self.trans.transliterate("pera")
        print(f"DEBUG: pera -> {res}")
        
        res = self.trans.transliterate("somossa")
        print(f"DEBUG: somossa -> {res}")

if __name__ == '__main__':
    unittest.main()
