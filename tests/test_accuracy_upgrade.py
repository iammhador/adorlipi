import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from core.engine.transliterator import Transliterator


ROOT = Path(__file__).resolve().parents[1]


class AccuracyUpgradeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._old_home = os.environ.get("HOME")
        cls._tmp_home = tempfile.TemporaryDirectory()
        os.environ["HOME"] = cls._tmp_home.name
        cls.transliterator = Transliterator()

    @classmethod
    def tearDownClass(cls):
        if cls._old_home is None:
            os.environ.pop("HOME", None)
        else:
            os.environ["HOME"] = cls._old_home
        cls._tmp_home.cleanup()

    def test_dictionary_and_loanword_json_are_valid(self):
        for relative_path in ["data/dictionary.json", "data/loanwords.json"]:
            with self.subTest(path=relative_path):
                path = ROOT / relative_path
                duplicate_keys = []

                def detect_duplicates(pairs):
                    seen = set()
                    for key, _value in pairs:
                        if key in seen:
                            duplicate_keys.append(key)
                        seen.add(key)
                    return dict(pairs)

                data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=detect_duplicates)
                non_ascii_keys = [key for key in data if re.search(r"[^\x00-\x7f]", key)]

                self.assertEqual([], duplicate_keys)
                self.assertEqual([], non_ascii_keys)

    def test_compound_suffix_composition(self):
        cases = {
            "phone-er": "ফোনের",
            "client-ra": "ক্লায়েন্টরা",
            "bag-ta": "ব্যাগটা",
            "office-e": "অফিসে",
            "Meeting-e": "মিটিংয়ে",
            "happiness-guloi": "হ্যাপিনেসগুলোই",
            "support-er": "সাপোর্টের",
            "cha-r": "চায়ের",
            "team-er": "টিমের",
        }

        for banglish, bangla in cases.items():
            with self.subTest(banglish=banglish):
                self.assertEqual(bangla, self.transliterator.transliterate(banglish))

    def test_plain_suffix_composition_uses_roots(self):
        cases = {
            "chabir": "চাবির",
            "supporter": "সাপোর্টের",
        }

        for banglish, bangla in cases.items():
            with self.subTest(banglish=banglish):
                self.assertEqual(bangla, self.transliterator.transliterate(banglish))

    def test_english_loanword_fallback(self):
        cases = {
            "wallet": "ওয়ালেট",
            "cloudy": "ক্লাউডি",
            "question": "কোয়েশ্চেন",
            "support": "সাপোর্ট",
            "performance": "পারফরম্যান্স",
            "time": "টাইম",
            "team": "টিম",
            "catalog": "ক্যাটালগ",
            "network": "নেটওয়ার্ক",
            "connection": "কানেকশন",
            "librarian": "লাইব্রেরিয়ান",
            "quiet": "কোয়াইট",
            "concentration": "কনসেন্ট্রেশন",
            "window": "উইন্ডো",
            "study": "স্টাডি",
            "owner": "ওনার",
            "news": "নিউজ",
            "dinner": "ডিনার",
            "reference": "রেফারেন্স",
            "pastry": "পেস্ট্রি",
            "guide": "গাইড",
            "loud": "লাউড",
            "new": "নিউ",
        }

        for english, bangla in cases.items():
            with self.subTest(english=english):
                self.assertEqual(bangla, self.transliterator.transliterate(english))

    def test_basic_banglish_regressions_from_generated_paragraph(self):
        cases = {
            "khujte": "খুঁজতে",
            "baierer": "বাইরের",
            "dhuklam": "ঢুকলাম",
            "hochhilo": "হচ্ছিলো",
            "bhanglo": "ভাঙলো",
            "bunch": "গোছা",
            "pouchanor": "পৌঁছানোর",
            "mile": "মিলে",
            "komar": "কমার",
            "bon-er": "বোনের",
            "kinte": "কিনতে",
            "banie": "বানিয়ে",
            "rekheche": "রেখেছে",
            "pouchiye": "পৌঁছে",
            "boshar": "বসার",
            "korchhilo": "করছিলো",
            "jachhilo": "যাচ্ছিলো",
            "lagchhilo": "লাগছিলো",
            "noshtho": "নষ্ট",
            "sekhaney": "সেখানে",
            "pasher": "পাশের",
            "Rafi": "রাফি",
            "rekhechen": "রেখেছেন",
        }

        for banglish, bangla in cases.items():
            with self.subTest(banglish=banglish):
                self.assertEqual(bangla, self.transliterator.transliterate(banglish))

    def test_generated_multiline_benchmark_has_no_english_leaks(self):
        base_lines = [
            "phone-er battery dead chhilo kintu charger table-er upor chhilo",
            "client-ra question korlo kintu performance really impressive chhilo",
            "wallet bag-ta office-e rekhe team-er support nilam",
            "cloudy weather-e family-r sathe cha-r cup kheye stress komlo",
            "happiness-guloi support-er moto kaj kore",
            "deadline upcoming project-er jonno time update korte hobe",
            "chabir bunch file-er pashe chhilo",
            "supporter crowd difficult holeo manager satisfied holo",
        ]
        text = "\n".join(base_lines * 15)
        output = self.transliterator.transliterate(text)

        self.assertEqual(120, len(output.splitlines()))
        self.assertIsNone(re.search(r"[A-Za-z]", output))
        self.assertIn("ফোনের ব্যাটারি ডেড", output)
        self.assertIn("ক্লায়েন্টরা কোয়েশ্চেন করলো", output)
        self.assertIn("ওয়ালেট ব্যাগটা অফিসে", output)
        self.assertIn("ফ্যামিলির সাথে চায়ের কাপ", output)
        self.assertIn("ডেডলাইন আপকামিং প্রজেক্টের", output)

    def test_audit_tool_reports_source_layers(self):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as f:
            f.write("phone-er wallet randomword")
            path = f.name

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "audit_transliteration.py"), path],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
        finally:
            os.unlink(path)

        lines = result.stdout.strip().splitlines()
        self.assertEqual(
            "input\tcurrent_output\tsource_layer\tconfidence\tmatched_key\tdictionary_hit\tsuspected_bad",
            lines[0],
        )
        self.assertTrue(
            any(line.startswith("phone-er\tফোনের\tcompound_suffix_dictionary_root\t") for line in lines)
        )
        self.assertTrue(any(line.startswith("wallet\tওয়ালেট\tloanword\t") for line in lines))
        self.assertTrue(any(line.startswith("randomword\t") for line in lines))

    def test_library_paragraph_regression_samples(self):
        text = (
            "catalog search korte network connection slow chhilo. "
            "Librarian apu quiet corner-e boshar permission dilen. "
            "Window-r glass-e sound peaceful lagchhilo. "
            "Study sesh kore owner-er cafe-te dinner news dekhlam."
        )
        output = self.transliterator.transliterate(text)

        self.assertIsNone(re.search(r"[A-Za-z]", output))
        self.assertIn("ক্যাটালগ সার্চ করতে নেটওয়ার্ক কানেকশন স্লো ছিলো", output)
        self.assertIn("লাইব্রেরিয়ান আপু কোয়াইট কর্নারে বসার পারমিশন দিলেন", output)
        self.assertIn("উইন্ডোর গ্লাসে সাউন্ড পিসফুল লাগছিলো", output)
        self.assertIn("স্টাডি শেষ করে ওনারের ক্যাফেতে ডিনার নিউজ দেখলাম", output)

    def test_conversational_patch_entries_and_source_layers(self):
        cases = {
            "bhasha": "ভাষা",
            "bhashar": "ভাষার",
            "bhashay": "ভাষায়",
            "khaisi": "খাইসি",
            "gesi": "গেছি",
            "gesilo": "গেছিলো",
            "youtubee": "ইউটিউবে",
            "internete": "ইন্টারনেটে",
        }

        for banglish, bangla in cases.items():
            with self.subTest(banglish=banglish):
                info = self.transliterator.explain_word(banglish)
                self.assertEqual(bangla, info["current_output"])
                self.assertEqual("dictionary", info["source_layer"])
                self.assertGreaterEqual(info["confidence"], 0.99)
                self.assertTrue(info["matched_key"])

    def test_dictionary_whitespace_cleanup_regressions(self):
        cases = {
            "dekhchi": "দেখছি",
            "recently": "রিসেন্টলি",
            "obhinoy": "অভিনয়",
            "shunchi": "শুনছি",
            "bf": "বয়ফ্রেন্ড",
        }

        for banglish, bangla in cases.items():
            with self.subTest(banglish=banglish):
                info = self.transliterator.explain_word(banglish)
                self.assertEqual(bangla, info["current_output"])
                self.assertEqual("dictionary", info["source_layer"])

    def test_gated_fallbacks_block_bad_substitutions(self):
        forbidden = {
            "trishna": "বিতৃষ্ণা",
            "khomota": "অক্ষমতা",
            "mantri": "মানতি",
        }

        for banglish, wrong in forbidden.items():
            with self.subTest(banglish=banglish):
                info = self.transliterator.explain_word(banglish)
                self.assertNotEqual(wrong, info["current_output"])
                self.assertNotEqual("fuzzy_dictionary", info["source_layer"])

    def test_phonetic_fallback_conjunct_word_normalization(self):
        cases = {
            "mrityu": "মৃত্যু",
            "prarthona": "প্রার্থনা",
            "sanskriti": "সংস্কৃতি",
        }

        for banglish, bangla in cases.items():
            with self.subTest(banglish=banglish):
                info = self.transliterator.explain_word(banglish)
                self.assertEqual(bangla, info["current_output"])
                self.assertEqual("phonetic", info["source_layer"])
                self.assertLess(info["confidence"], 0.9)
                self.assertEqual(banglish, info["matched_key"])

    def test_explain_word_includes_confidence_and_match_metadata(self):
        dictionary_info = self.transliterator.explain_word("bhasha")
        self.assertIn("confidence", dictionary_info)
        self.assertIn("matched_key", dictionary_info)
        self.assertIsInstance(dictionary_info["confidence"], float)
        self.assertEqual("bhasha", dictionary_info["matched_key"])

        fuzzy_or_phonetic = self.transliterator.explain_word("randomword")
        self.assertIn("confidence", fuzzy_or_phonetic)
        self.assertIn("matched_key", fuzzy_or_phonetic)

    def test_suggestion_smoke_is_stable_and_bangla_only(self):
        suggestions = self.transliterator.get_suggestions("bhasha")
        self.assertLessEqual(len(suggestions), 5)
        self.assertEqual(len(suggestions), len(set(suggestions)))
        for item in suggestions:
            with self.subTest(item=item):
                self.assertIsNone(re.search(r"[A-Za-z]", item))


if __name__ == "__main__":
    unittest.main()
