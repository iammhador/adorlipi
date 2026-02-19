import json
import os

DICT_PATH = "../data/dictionary.json"

# Phase 12: Emphatic Words (Ending in 'i', 'o', 'ei', 'lei')
# These are very common in spoken/social Banglish but often missed by simple phonetic rules.
bulk_data_12 = {
    # -ei (Emphasis)
    "korei": "করেই", "bolei": "বলেই", "dekhlei": "দেখলেই", "shunlei": "শুনলেই",
    "khelei": "খেলেই", "gelei": "গেলেই", "elei": "এলেই", "pelei": "পেলেই",
    "dilei": "দিলেই", "nilei": "নিলেই", "holei": "হলেই", "thaklei": "থাকলেই",
    "parlei": "পারলেই", "anlei": "আনলেই", "janlei": "জানলেই", "bujhlei": "বুঝলেই",
    "chailei": "চাইলেই", "bollei": "বল্লেই", "korlei": "করলেই",
    
    # -i (Emphasis / Exclusion)
    "ami-i": "আমিই", "tumi-i": "তুমিই", "she-i": "সে-ই", "tai": "তাই",
    "eita-i": "এইটাই", "oita-i": "ওইটাই", "ekhoni": "এখনই", "tokhoni": "তখনই",
    
    # -o (Also / Given that)
    "ateo": "এতেও", "oteo": "ওতেও", "koreo": "করেও", "boleo": "বলেও",
    "dekheo": "দেখেও", "shuneo": "শুনেও", "kheyeo": "খেয়েও", "giyeo": "গিয়েও",
    "eseo": "এসেও", "peyeo": "পেয়েও", "diyeo": "দিয়েও", "niyeo": "নিয়েও",
    "holeo": "হলেও", "thakleo": "থাকলেও", "parleo": "পারলেও", "anleo": "আনলেও",
    "janleo": "জানলেও", "bujhleo": "বুঝলেও", "chaileo": "চাইলেও",
    
    # Common variations
    "bolle": "বললে", "korle": "করলে", "dekhle": "দেখলে", "shunle": "শুনলে",
    "khele": "খেলে", "gele": "গেলে", "ele": "এলে", "pele": "পেলে",
    "dile": "দিলে", "nile": "নিলে", "hole": "হলে", "thakle": "থাকলে",
    "parle": "পারলে", "anle": "আনলে", "janle": "জানলে", "bujhle": "বুঝলে",
    "chaile": "চাইলে",
    
    # Extra common social words
    "asholei": "আসলেই", "sotti": "সত্যি", "shotti": "সত্যি", "sottiy": "সত্যিই",
    "bujhso": "বুঝছো", "bujhcho": "বুঝছো", "bujhsi": "বুঝছি", "bujhchi": "বুঝছি",
    "parso": "পারছো", "parcho": "পারছো", "parsi": "পারছি", "parchi": "পারছি",
    "korso": "করছো", "korcho": "করছো", "korsi": "করছি", "korchi": "করছি",
    "khacchi": "খাচ্ছি", "jacchi": "যাচ্ছি", "dheke": "দেখে", # typo correction often needed
    "thik": "ঠিক", "thikase": "ঠিক আছে", "thikache": "ঠিক আছে",
}

def load_dict(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_dict(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)

def main():
    print(f"Loading dictionary from {DICT_PATH}...")
    current_dict = load_dict(DICT_PATH)
    initial_count = len(current_dict)
    
    print(f"Current entry count: {initial_count}")
    
    added_count = 0
    skipped_count = 0
    
    # Process Phase 12
    print("\nProcessing Bulk Import Phase 12 (Emphatic & Social Variations)...")
    for eng, bng in bulk_data_12.items():
        eng_lower = eng.lower().strip()
        # For emphatic words, we might want to overwrite if the previous one was just a phonetic guess
        # But generally, if it's in dict, it's likely manual.
        # Let's check if it exists.
        if eng_lower not in current_dict:
            current_dict[eng_lower] = bng
            added_count += 1
        else:
            # Check if we should update. logic: if current val is VERY different/wrong?
            # For now, safe default is skip if exists.
            # actually, for 'bolle', phonetic might give 'বল্লে' (bol-le), standard might be 'বললে'.
            # Let's force update specific ones if we are sure.
            # Current policy: First entry wins usually.
            skipped_count += 1
            
    print(f"\nAdded: {added_count}")
    print(f"Skipped (already existed): {skipped_count}")
    
    if added_count > 0:
        save_dict(DICT_PATH, current_dict)
        print(f"Successfully saved updated dictionary to {DICT_PATH}")
    else:
        print("No new words to save.")
        
    final_count = len(current_dict)
    print(f"Final dictionary size: {final_count}")

if __name__ == "__main__":
    main()
