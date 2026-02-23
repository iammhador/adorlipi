import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.engine.phonetic_parser import PhoneticParser

class TestPhoneticHeuristics(unittest.TestCase):
    def setUp(self):
        # We test ONLY the PhoneticParser (no dictionary)
        self.parser = PhoneticParser("data/mapping.json")

    def test_algorithmic_conjuncts(self):
        cases = {
            "shanto": "শান্ত",
            "bandhob": "বান্ধব",
            "ononto": "অনন্ত",
            "kkhoti": "ক্ষোতি",
            "shikkhok": "শিক্ষক",
            "lomba": "লম্বা",
            "buddho": "বুদ্ধ",
            "kosto": "কস্ট", 
            "rasta": "রাস্টা", # Without dict st -> স্ট
            "gonj": "গঞ্জ",
            "ponchash": "পঞ্চাশ",
            "iccha": "ইচ্ছা",
            "songgram": "সংগ্রাম"
        }
        
        for inp, expected in cases.items():
            with self.subTest(input=inp):
                # Verify that the direct parsed output matches expected 
                # (minus intrinsic 'o' handling at boundaries which might differ slightly)
                # But our O-dropping logic should handle it!
                res = self.parser.parse(inp)
                self.assertEqual(res, expected)

if __name__ == '__main__':
    unittest.main()
