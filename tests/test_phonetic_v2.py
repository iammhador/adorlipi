import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.engine.phonetic_parser import PhoneticParser

class TestPhoneticV2(unittest.TestCase):
    def setUp(self):
        self.parser = PhoneticParser('data/mapping.json')

    def test_smart_o_dropping(self):
        # 'o' in the middle of a consonant cluster should drop the O-kar
        self.assertEqual(self.parser.parse("khorgos"), "খরগস") # Dictionary handles খরগোস
        self.assertEqual(self.parser.parse("khorgosh"), "খরগশ") # Dictionary handles খরগোশ
        self.assertEqual(self.parser.parse("pagol"), "পাগল")
        self.assertEqual(self.parser.parse("chagol"), "ছাগল")
        self.assertEqual(self.parser.parse("kapor"), "কাপর") # Phonetically কাপর, dictionary handles কাপড়
        self.assertEqual(self.parser.parse("ador"), "আদর")
        self.assertEqual(self.parser.parse("kamon"), "কামন") # Dict handles কমন
        self.assertEqual(self.parser.parse("shokal"), "শোকাল") # Dict handles সকাল

    def test_explicit_o_kar(self):
        # 'o' at the end of a word or start of a word should keep the O-kar (if start, maps to অ usually)
        self.assertEqual(self.parser.parse("bhalo"), "ভালো")
        self.assertEqual(self.parser.parse("kholo"), "খোলো")
        self.assertEqual(self.parser.parse("onek"), "অনেক")
        self.assertEqual(self.parser.parse("ojogor"), "অজোগর") 

    def test_ref_regulation(self):
        # 'r' should not blindly form a Ref if preceded by an implicit vowel drop
        self.assertEqual(self.parser.parse("khorgos"), "খরগস")
        self.assertEqual(self.parser.parse("khorgosh"), "খরগশ")
        
        # Explicit spelling forcing a Ref might be 'rr' or relying on dictionary
        self.assertEqual(self.parser.parse("torko"), "তরকো")
        self.assertEqual(self.parser.parse("murokho"), "মুরোখো")

if __name__ == '__main__':
    unittest.main()
