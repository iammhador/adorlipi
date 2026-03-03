import re
import json
import os
import sys
import difflib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.engine.transliterator import Transliterator

def evaluate():
    filepath = "/home/onism/LOG FILE/__ ADOR __/test.txt"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    blocks = content.split('\n\n')
    bangla_truth = blocks[0].replace("Bangla:", "").strip()
    banglish_input = blocks[1].replace("Banglish:", "").strip()

    b_words = bangla_truth.split()
    e_words = banglish_input.split()

    b_clean = [re.sub(r'[^\w\s\u0980-\u09FF]', '', w) for w in b_words]
    b_clean = [w for w in b_clean if w]

    e_clean = [re.sub(r'[^\w\s]', '', w).lower() for w in e_words]
    e_clean = [w for w in e_clean if w]

    engine = Transliterator()
    a_words = [engine.transliterate(w) for w in e_clean]

    matcher = difflib.SequenceMatcher(None, a_words, b_clean)
    
    correct = 0
    mismatches = {}

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            correct += (i2 - i1)
        else:
            # Pair up mismatched sub-blocks safely
            for idx in range(max(i2 - i1, j2 - j1)):
                if i1 + idx < i2 and j1 + idx < j2:
                    banglish = e_clean[i1 + idx]
                    expected = b_clean[j1 + idx]
                    actual = a_words[i1 + idx]
                    if expected != actual:
                        mismatches[banglish] = expected

    total = len(e_clean)
    accuracy = (correct / total) * 100
    
    print(f"\n--- RESULTS ---")
    print(f"Total Evaluated Words: {total}")
    print(f"Perfect Matches: {correct}")
    print(f"Accuracy: {accuracy:.2f}%\n")
    
    print(f"Identified {len(mismatches)} missing/incorrect dictionary mappings.")

    # Save missing words to JSON for review
    with open("/home/onism/LOG FILE/__ ADOR __/data/missing_words.json", "w", encoding="utf-8") as f:
        json.dump(mismatches, f, ensure_ascii=False, indent=4)
        
    print(f"Saved {len(mismatches)} missing words to data/missing_words.json for your review.")

if __name__ == "__main__":
    evaluate()
