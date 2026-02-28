
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.engine.phonetic_parser import PhoneticParser

def test_words():
    parser = PhoneticParser('data/mapping.json')
    words = ["amar", "naam", "holo", "ador"]
    for w in words:
        print(f"'{w}' -> '{parser.parse(w)}'")

if __name__ == "__main__":
    test_words()
