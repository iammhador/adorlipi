
import unittest
from adorlipi.engine.transliterator import Transliterator

class TestRobustnessV2(unittest.TestCase):
    def setUp(self):
        self.trans = Transliterator()

    def test_ba_fola_w(self):
        # s + w -> স + ◌্ব = স্ব
        # swadhin -> স্বাধীন
        res = self.trans.transliterate("swadhin")
        print(f"DEBUG: swadhin -> {res}")
        self.assertEqual(res, "স্বাধীন")
        
        # bishwas -> বিশ্বাস
        res = self.trans.transliterate("bishwas")
        print(f"DEBUG: bishwas -> {res}")
        self.assertEqual(res, "বিশ্বাস")

    def test_ya_fola_variations(self):
        # k + y -> ক্যা
        res = self.trans.transliterate("kya")
        self.assertEqual(res, "ক্যা")
        
        # s + z -> স্য
        res = self.trans.transliterate("sz")
        self.assertEqual(res, "স্য")
        
        # somossha -> সমস্যা
        res = self.trans.transliterate("somossa")
        self.assertEqual(res, "সমস্যা")

    def test_ra_fola(self):
        # p + r -> প্র
        res = self.trans.transliterate("prothom")
        self.assertEqual(res, "প্রথম")

if __name__ == '__main__':
    unittest.main()
