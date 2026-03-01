
import sys
import os
import unittest

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.engine.phonetic_parser import PhoneticParser
from core.engine.transliterator import Transliterator

class TestRobustness(unittest.TestCase):
    def setUp(self):
        self.parser = PhoneticParser("data/mapping.json")
        self.trans = Transliterator() 

    def test_v_mapping(self):
        res = self.trans.transliterate("v")
        self.assertEqual(res, "ভ")
        
        res = self.trans.transliterate("faravi")
        self.assertEqual(res, "ফারাভি")

    def test_ya_fola(self):
        res = self.trans.transliterate("kya")
        self.assertEqual(res, "ক্যা")
        
        res = self.trans.transliterate("zy")
        self.assertEqual(res, "য্য")

    def test_ra_fola(self):
        res = self.trans.transliterate("pr")
        self.assertEqual(res, "প্র")
        
        res = self.trans.transliterate("br")
        self.assertEqual(res, "ব্র")
        
        res = self.trans.transliterate("pr")
        self.assertEqual(res, "প্র")

if __name__ == '__main__':
    unittest.main()
