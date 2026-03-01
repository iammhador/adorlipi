import json
import os
import sys

# Ensure imports work from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.engine.phonetic_parser import PhoneticParser

def main():
    dict_path = 'data/dictionary.json'
    words_file = 'new_words.txt'

    with open(dict_path, 'r', encoding='utf-8') as f:
        existing_dict = json.load(f)

    with open(words_file, 'r', encoding='utf-8') as f:
        new_words_raw = f.read().splitlines()

    print(f"Loaded existing dictionary with {len(existing_dict)} entries.")
    print(f"Loaded new words file with {len(new_words_raw)} lines.")

    import re
    # Clean and deduplicate words from all lines
    db_words = set()
    for line in new_words_raw:
        # Extract all purely alphabetical substrings from the line
        tokens = re.findall(r'[a-zA-Z]+', line.lower())
        for w in tokens:
            if len(w) > 1:  # Ignore 1-letter noise usually
                db_words.add(w)

    print(f"Total unique alphabetical words in new_words.txt: {len(db_words)}")

    # Isolate strictly new words not in our dictionary
    words_to_add = []
    for w in db_words:
        if w not in existing_dict:
            words_to_add.append(w)

    print(f"Identified {len(words_to_add)} completely new words to process and add.")

    if not words_to_add:
        print("Dictionary already contains all these words!")
        return

    # Initialize V2 Engine to algorithmically generate the spellings for new words
    parser = PhoneticParser('data/mapping.json')
    
    # Process the new words
    added_count = 0
    print("Processing words through V2 phonetic engine...")
    for i, banglish_word in enumerate(words_to_add):
        # The parser intrinsically returns perfectly parsed Bengali without dictionary lookup
        bengali_word = parser.parse(banglish_word)
        existing_dict[banglish_word] = bengali_word
        added_count += 1
        
        if i % 5000 == 0 and i > 0:
            print(f"  Processed {i}/{len(words_to_add)} words...")

    # Sort the dictionary alphabetically for clean JSON output
    sorted_dict = dict(sorted(existing_dict.items()))

    # Save back to dictionary.json
    with open(dict_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_dict, f, ensure_ascii=False, indent=4)

    print(f"\nSuccessfully added {added_count} new words to data/dictionary.json!")
    print(f"Total Dictionary Size is now: {len(sorted_dict)} words.")

if __name__ == "__main__":
    main()
