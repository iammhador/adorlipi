#!/usr/bin/env python3
import argparse
import os
import re
import sys


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from core.engine.transliterator import Transliterator


def iter_words(text, unique):
    seen = set()
    for match in re.finditer(r"[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)*", text):
        word = match.group(0)
        key = word.lower()
        if unique and key in seen:
            continue
        seen.add(key)
        yield word


def main():
    parser = argparse.ArgumentParser(description="Audit Banglish transliteration word by word.")
    parser.add_argument("path", help="Text file to audit")
    parser.add_argument("--all", action="store_true", help="Show repeated words instead of unique words only")
    args = parser.parse_args()

    with open(args.path, "r", encoding="utf-8") as f:
        text = f.read()

    transliterator = Transliterator()
    print("input\tcurrent_output\tsource_layer\tconfidence\tmatched_key\tdictionary_hit\tsuspected_bad")
    for word in iter_words(text, unique=not args.all):
        info = transliterator.explain_word(word)
        print(
            f"{info['input']}\t"
            f"{info['current_output']}\t"
            f"{info['source_layer']}\t"
            f"{info['confidence']}\t"
            f"{info['matched_key']}\t"
            f"{str(info['dictionary_hit']).lower()}\t"
            f"{str(info['suspected_bad']).lower()}"
        )


if __name__ == "__main__":
    main()
