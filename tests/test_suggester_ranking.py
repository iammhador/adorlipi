import json
import tempfile
import unittest
from pathlib import Path

from core.engine.suggester import Suggester


class _DummyContext:
    def __init__(self, boosted_word):
        self.boosted_word = boosted_word

    def score_boost(self, word):
        return 80 if word == self.boosted_word else 0


class SuggesterRankingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)

        openbangla = {
            "v": [
                "ভালো",
                "ভালোই",
                "ভালোর",
                "ভালোবাসি",
                "ভালোবাসা",
                "ভালোকথা",
                "ভালোত্ব",
            ],
            "k": [f"কাব{idx:03d}" for idx in range(120)] + ["কামনা", "কামরান", "কামরুল"],
        }
        word_frequency = {
            "ভালোই": 70,
            "ভালোর": 60,
            "ভালোবাসি": 75,
            "ভালোবাসা": 90,
            "ভালোকথা": 8,
            "ভালোত্ব": 5,
            "কামনা": 120,
            "কামরান": 40,
            "কামরুল": 35,
        }
        conversational = {
            "bhalo": "ভালো",
            "bhaloi": "ভালোই",
            "bhalobasi": "ভালোবাসি",
            "valor": "ভালোর",
            "kamona": "কামনা",
        }

        (self.base / "openbangla_dictionary.json").write_text(
            json.dumps(openbangla, ensure_ascii=False), encoding="utf-8"
        )
        (self.base / "word_frequency.json").write_text(
            json.dumps(word_frequency, ensure_ascii=False), encoding="utf-8"
        )
        (self.base / "dictionary.json").write_text(
            json.dumps(conversational, ensure_ascii=False), encoding="utf-8"
        )

        self.suggester = Suggester(
            data_path=str(self.base / "openbangla_dictionary.json"),
            conversational_data_path=str(self.base / "dictionary.json"),
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_conversational_short_words_rank_higher(self):
        suggestions = self.suggester.get_suggestions("bhalo", "ভালো")
        self.assertTrue(suggestions)
        self.assertEqual("ভালোই", suggestions[0])
        self.assertIn("ভালোবাসি", suggestions)

    def test_context_boost_reorders_results(self):
        self.suggester.set_context_engine(_DummyContext("ভালোবাসি"))
        suggestions = self.suggester.get_suggestions("bhalo", "ভালো")
        self.assertTrue(suggestions)
        self.assertEqual("ভালোবাসি", suggestions[0])

    def test_prefix_range_does_not_drop_late_entries(self):
        suggestions = self.suggester.get_suggestions("kam", "কাম")
        self.assertTrue(suggestions)
        self.assertEqual("কামনা", suggestions[0])


if __name__ == "__main__":
    unittest.main()
