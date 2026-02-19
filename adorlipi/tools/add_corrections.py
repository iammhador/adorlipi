
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
    "aapni": "আপনি",
    "abba": "আব্বা",
    "ammu": "আম্মু",
    "kormo": "কর্ম",
    "hotat": "হঠাৎ",
    "hoqaq": "হঠাৎ",
    # Ya-fola
    "kyash": "ক্যাশ",
    "pyaket": "প্যাকেট",
    "byakkha": "ব্যাখ্যা",
    "obhyas": "অভ্যাস",
    "konnya": "কন্যা",
    "bonno": "বন্য",
    "shosso": "শস্য",
    "sojjo": "সহ্য",
    "drishsho": "দৃশ্য",
    "babsha": "ব্যবসা",
    # Ra-fola
    "gram": "গ্রাম",
    "pran": "প্রাণ",
    "tran": "ত্রাণ",
    "broto": "ব্রত",
    "bhramyoman": "ভ্রাম্যমাণ",
    "priti": "প্রীতি",
    "prochar": "প্রচার",
    "chatro": "ছাত্র",
    "matro": "মাত্র",
    "patro": "পাত্র",
    # Ba-fola
    "swagotom": "স্বাগতম",
    "dhongso": "ধ্বংস",
    "bishsho": "বিশ্ব",
    "swor": "স্বর",
    "swami": "স্বামী",
    "swocchondo": "স্বচ্ছন্দ",
    "jwor": "জ্বর",
    "dwip": "দ্বীপ",
    "dwitiyo": "দ্বিতীয়",
    "twok": "ত্বক"
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
