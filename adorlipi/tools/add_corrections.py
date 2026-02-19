
import json

# Corrections for slang and common words
CORRECTIONS = {
    "somosssa": "সমস্যা",
    "somossa": "সমস্যা",
    "problem": "সমস্যা",
    "shomossha": "সমস্যা",
    "soomosha": "সমস্যা",
    "somosha": "সমস্যা",
    "pera": "প্যারা",
    "para": "প্যারা",
    "chill": "চিল",
    "osthir": "অস্থির",
    "aam": "আম",
    "aapni": "আপনি"
}

DICT_PATH = "../data/dictionary.json"

def update_dictionary():
    try:
        with open(DICT_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        print(f"Current dictionary size: {len(data)}")
        
        added_count = 0
        for word, bangla in CORRECTIONS.items():
            if word not in data:
                data[word] = bangla
                added_count += 1
            elif data[word] != bangla:
                print(f"Updating {word}: {data[word]} -> {bangla}")
                data[word] = bangla
                added_count += 1
                
        with open(DICT_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"Added/Updated {added_count} words.")
        print(f"New dictionary size: {len(data)}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_dictionary()
