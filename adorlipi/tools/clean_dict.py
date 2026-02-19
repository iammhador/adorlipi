import json
import re
from collections import defaultdict

# The dirty dictionary content from banglish_mvp (as read in previous turn)
# I will use the file path directly to ensure I get the latest.
SOURCE_FILE = "/home/onism/LOG FILE/__ ADOR __/banglish_mvp/data/dictionary.json"
TARGET_FILE_ADOR = "/home/onism/LOG FILE/__ ADOR __/adorlipi/data/dictionary.json"
TARGET_FILE_BANG = "/home/onism/LOG FILE/__ ADOR __/banglish_mvp/data/dictionary.json"

def clean_and_expand():
    # 1. Read raw lines to detect duplicates
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    key_tracker = defaultdict(list)
    clean_dict = {}
    
    # Simple regex to extract key-value from JSON lines
    # Assumes "key": "value" format (standard pretty print)
    pattern = re.compile(r'"([^"]+)":\s*"([^"]+)"')

    print("--- Duplicate Detection Report ---")
    duplicates_found = False
    
    for i, line in enumerate(lines):
        match = pattern.search(line)
        if match:
            key, value = match.groups()
            key = key.lower()
            key_tracker[key].append((i + 1, value))
            
            # Logic: Keep the LAST one usually, but let's notify
            clean_dict[key] = value

    for key, occurrences in key_tracker.items():
        if len(occurrences) > 1:
            duplicates_found = True
            lines_str = ", ".join([f"L{x[0]}({x[1]})" for x in occurrences])
            print(f"Duplicate '{key}': found at {lines_str}")

    if not duplicates_found:
        print("No duplicates found.")
        
    # 2. Add New Words (Expansion)
    new_words = {
        # Pronouns
        "tui": "তুই", "tor": "তোর", "toke": "তোকে",
        "tumra": "তোমরা", "tomader": "তোমাদের",
        "take": "তাকে", "tader": "তাদের", 
        "uni": "উনি", "unar": "উনার",
        
        # Questions
        "koi": "কই", "kon": "কোন", "konta": "কোনটা",
        "kobe": "কবে", "kokhon": "কখন",
        "kaw": "কাউ", "kake": "কাকে",
        
        # Verbs (Common casual)
        "hoise": "হয়েছে", "hobe": "হবে", 
        "partasi": "পারতেছি", "partsi": "পারছি",
        "parbo": "পারবো", "parbe": "পারবে",
        "chao": "চাও", "chai": "চাই",
        "jani": "জানি", "jano": "জানো",
        
        # Essentials
        "r": "আর", "naki": "নাকি",
        "eshob": "এসব", "ashole": "আসলে",
        "ektu": "একটু", "onek": "অনেক",
        "obossy": "অবশ্যই", "shob": "সব",
        "shobar": "সবার", "halka": "হালকা",
        "patla": "পাতলা", "oss": "অস্থির",
        "osthir": "অস্থির", "jo": "জো",
        "joss": "জোস", "pera": "পেরা",
        "mama": "মামা", "bro": "ব্রো",
        "dost": "দোস্ত",
        "bad": "বাদ", "thak": "থাক"
    }
    
    # Merge new words if not present
    added_count = 0
    for k, v in new_words.items():
        if k not in clean_dict:
            clean_dict[k] = v
            added_count += 1
            
    print(f"\n--- Expansion Report ---")
    print(f"Added {added_count} new words.")
    
    # 3. Sort and Save
    # Sort by key for easier reading
    sorted_dict = dict(sorted(clean_dict.items()))
    
    # Save to both locations
    def save_json(path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
    save_json(TARGET_FILE_ADOR, sorted_dict)
    save_json(TARGET_FILE_BANG, sorted_dict)
    print(f"\nSaved optimized dictionary to:\n- {TARGET_FILE_ADOR}\n- {TARGET_FILE_BANG}")

if __name__ == "__main__":
    clean_and_expand()
