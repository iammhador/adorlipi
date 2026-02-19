
import unittest
from adorlipi.engine.transliterator import Transliterator

class TestRobustnessV3(unittest.TestCase):
    def setUp(self):
        self.trans = Transliterator()

    def test_retroflexes(self):
        # tth -> ঠ
        self.assertEqual(self.trans.transliterate("tth"), "ঠ")
        # ddh -> ঢ
        self.assertEqual(self.trans.transliterate("ddh"), "ঢ")

    def test_nasals(self):
        # ng -> ং
        self.assertEqual(self.trans.transliterate("ng"), "ং")
        # nng -> ঙ
        self.assertEqual(self.trans.transliterate("nng"), "ঙ")

    def test_ri(self):
        # ri -> ঋ
        self.assertEqual(self.trans.transliterate("ri"), "ঋ")
        # kri -> কৃ
        self.assertEqual(self.trans.transliterate("kri"), "কৃ")

    def test_double_consonant(self):
        # abba -> আ+ব+্+ব+া = আব্বা
        res = self.trans.transliterate("abba")
        print(f"DEBUG: abba -> {res}")
        self.assertEqual(res, "আব্বা")
        
        # ammu -> আম্মু
        res = self.trans.transliterate("ammu")
        self.assertEqual(res, "আম্মু")
        
        # shotto -> সত্য (If s-h-o-t-t-o -> শ+ত+্+ত+ো = শত্তো or সত্য)
        # Traditionally shotto is শ+ত+্+য. But doubles are also common.
        self.assertEqual(self.trans.transliterate("ll"), "ল্ল")

    def test_ref(self):
        # rk -> র্ক
        # korma -> কর্ম (k-o-r-m-o)
        res = self.trans.transliterate("kormo")
        print(f"DEBUG: kormo -> {res}")
        self.assertEqual(res, "কর্ম")

    def test_khanda_ta(self):
        # q -> ৎ
        # hotat -> হঠাৎ
        self.assertEqual(self.trans.transliterate("hoqaq"), "হঠাৎ")

if __name__ == '__main__':
    unittest.main()
