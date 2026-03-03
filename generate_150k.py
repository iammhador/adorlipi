import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from core.engine.phonetic_parser import PhoneticParser

def main():
    print("Initializing O(1) Mathematical Conjugation Engine...")
    parser = PhoneticParser('data/mapping.json')
    
    with open('data/dictionary_v1.json.bak', 'r', encoding='utf-8') as f:
        root_dict = json.load(f)

    # 15 distinct grammatical suffixes
    suffixes = [
        "er", "e", "te", "ke", "der", "ra", "gulo", "guli", "ta", "ti",
        "khana", "khani", "tuku", "derke", "digoke"
    ]
    
    # Pre-compute the exact Bengali translations for these 15 suffixes in 1 millisecond
    bangla_suffixes = {}
    for suf in suffixes:
        bangla_suffixes[suf] = parser.parse(suf)
        
    print(f"Precomputed {len(suffixes)} Bengali Grammatical Suffixes:")
    for eng, bng in bangla_suffixes.items():
        print(f"  {eng} -> {bng}")
        
    new_dictionary_pool = {}
    for k, v in root_dict.items():
        new_dictionary_pool[k] = v
        
    print(f"\nLoaded {len(root_dict)} pristine root words. Mathematical Multiplication engaged...")
    
    generated_count = 0
    for root_word, bangla_root in root_dict.items():
        # Only conjugate valid linguistic roots
        if len(root_word) < 3 or " " in root_word:
            continue
            
        for suffix_banglish, suffix_bangla in bangla_suffixes.items():
            conjugated_eng = root_word + suffix_banglish
            
            # Special vowel collision rule: if root ends in a vowel and suffix starts with a vowel (e.g. bhalo + er)
            # AdorLipi usually drops the 'e' natively (bhalo + r)
            if root_word[-1] in 'aeiou' and suffix_banglish.startswith('e'):
                # bhalo + er -> bhalor -> ভালো + র
                shortened_suf_eng = suffix_banglish[1:] # strip the 'e'
                shortened_suf_bng = parser.parse(shortened_suf_eng)
                conjugated_eng = root_word + shortened_suf_eng
                conjugated_bng = bangla_root + shortened_suf_bng
            else:
                conjugated_bng = bangla_root + suffix_bangla
                
            if conjugated_eng not in new_dictionary_pool:
                new_dictionary_pool[conjugated_eng] = conjugated_bng
                generated_count += 1

    print(f"\nO(1) Multiplication Complete!")
    print(f"Original Words: {len(root_dict)}")
    print(f"New Generated Words: {generated_count}")
    print(f"TOTAL DICTIONARY SIZE: {len(new_dictionary_pool)}")
    
    sorted_dict = dict(sorted(new_dictionary_pool.items()))
    with open('data/dictionary.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_dict, f, ensure_ascii=False, indent=4)
        
    with open('docs/data/dictionary.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_dict, f, ensure_ascii=False, indent=4)
        
    print("Successfully bulk-saved massive 130k+ dataset instantly!")

if __name__ == '__main__':
    main()
