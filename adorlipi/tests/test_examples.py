import sys
import os
import unittest

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.transliterator import Transliterator

class TestBanglishMVP(unittest.TestCase):
    def setUp(self):
        self.engine = Transliterator()

    def test_basic_words(self):
        cases = {
            "Ami": "আমি",
            "Tumi": "তুমি",
            "Bhai": "ভাই",
            "Vai": "ভাই",
            "Bhaiya": "ভাইয়া"
        }
        for inp, expected in cases.items():
            with self.subTest(input=inp):
                self.assertEqual(self.engine.transliterate(inp), expected)

    def test_sentences(self):
        cases = {
            "Ami tomay bhalobashi": "আমি তোমায় ভালোবাসি",
            "Khub valo": "খুব ভালো", 
            "Tmi kothay": "তুমি কোথায়"
        }
        for inp, expected in cases.items():
            with self.subTest(input=inp):
                self.assertEqual(self.engine.transliterate(inp), expected)

if __name__ == '__main__':
    unittest.main()
