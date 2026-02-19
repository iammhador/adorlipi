
import unittest
from adorlipi.engine.phonetic_parser import PhoneticParser
from adorlipi.engine.transliterator import Transliterator

class TestRobustness(unittest.TestCase):
    def setUp(self):
        self.parser = PhoneticParser("adorlipi/data/mapping.json")
        # Ensure we test the parser logic directly or via transliterator
        self.trans = Transliterator() 

    def test_v_mapping(self):
        # v -> ভ
        res = self.trans.transliterate("v")
        self.assertEqual(res, "ভ")
        
        # faravi -> ফারাবি (if b) or ফারাভি (if v)
        # f -> ফ, a -> া, r -> র, a -> া, v -> ভ, i -> ি
        res = self.trans.transliterate("faravi")
        self.assertEqual(res, "ফারাভি")

    def test_ya_fola(self):
        # kya -> ক + ◌্য + া = ক্যা
        # k -> ক (cons)
        # y -> ◌্য (ya-fola) because last was k
        # a -> া (kar)
        res = self.trans.transliterate("kya")
        self.assertEqual(res, "ক্যা")
        
        # zy -> জ + ◌্য = জ্য
        res = self.trans.transliterate("zy")
        self.assertEqual(res, "জ্য")

    def test_ra_fola(self):
        # pr -> প + ◌্র = প্র
        res = self.trans.transliterate("pr")
        self.assertEqual(res, "প্র")
        
        # br -> ব + ◌্র = ব্র
        res = self.trans.transliterate("br")
        self.assertEqual(res, "ব্র")
        
        # prothom -> প্র + o(kar?) + ...
        # If o -> Kar, then প্রোথম.
        # If user wants প্রথম, usually strict engines require 'pr' + implicit?
        # Let's just check 'pr' formation for now.
        res = self.trans.transliterate("pr")
        self.assertEqual(res, "প্র")

if __name__ == '__main__':
    unittest.main()
