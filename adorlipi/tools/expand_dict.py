import json
import os

DICT_PATH = "../data/dictionary.json"

# New words to add (English -> Bangla phonetic/transliteration)
new_words = {
    # Banglish Common
    "amar": "আমার",
    "kothay": "কোথায়",
    "kemne": "কেমনে",
    "kivabe": "কিভাবে",
    "kobe": "কবে",
    "khub": "খুব",
    "onek": "অনেক",
    "shundor": "সুন্দর",
    "dhonnobad": "ধন্যবাদ",
    "swag": "স্বাগ",
    "osthir": "অস্থির",
    "joss": "জোস",
    "baje": "বাজে",
    "faltu": "ফালতু",
    "sera": "সেরা",
    "moja": "মজা",
    "hashi": "হাসি",
    "kanna": "কান্নাকাটি",
    "kosto": "কষ্ট",
    "dukho": "দুঃখ",
    "shukh": "সুখ",
    "shanti": "শান্তি",
    "bhalobasha": "ভালোবাসা",
    "premm": "প্রেম",
    "biye": "বিয়ে",
    "bou": "বউ",
    "jamai": "জামাই",
    "baba": "বাবা",
    "ma": "মা",
    "bhai": "ভাই",
    "bon": "বোন",
    "dada": "দাদা",
    "dadi": "দাদি",
    "nana": "নানা",
    "nani": "নানি",
    "bondhu": "বন্ধু",
    "shatru": "শত্রু",
    
    # Common English specific needs
    "facebook": "ফেইসবুক",
    "google": "গুগল",
    "youtube": "ইউটিউব",
    "internet": "ইন্টারনেট",
    "online": "অনলাইন",
    "offline": "অফলাইন",
    "download": "ডাউনলোড",
    "upload": "আপলোড",
    "click": "ক্লিক",
    "link": "লিংক",
    "share": "শেয়ার",
    "like": "লাইক",
    "comment": "কমেন্ট",
    "status": "স্ট্যাটাস",
    "story": "স্টোরি",
    "post": "পোস্ট",
    "profile": "প্রোফাইল",
    "picture": "পিকচার",
    "pic": "পিক",
    "image": "ইমেজ",
    "video": "ভিডিও",
    "audio": "অডিও",
    "camera": "ক্যামেরা",
    "phone": "ফোন",
    "call": "কল",
    "sms": "এসএমএস",
    "text": "টেক্সট",
    "number": "নাম্বার",
    "sim": "সিম",
    "recharge": "রিচার্জ",
    "mb": "এমবি",
    "gb": "জিবি",
    "data": "ডাটা",
    "wifi": "ওয়াইফাই",
    "password": "পাসওয়ার্ড",
    "login": "লগইন",
    "logout": "লগআউট",
    "signup": "সাইনআপ",
    "register": "রেজিস্টার",
    
    # Daily Life English
    "school": "স্কুল",
    "college": "কলেজ",
    "university": "ইউনিভার্সিটি",
    "varsity": "ভার্সিটি",
    "office": "অফিস",
    "bank": "ব্যাংক",
    "market": "মার্কেট",
    "bazar": "বাজার",
    "shop": "শপ",
    "store": "স্টোর",
    "shopping": "শপিং",
    "bus": "বাস",
    "train": "ট্রেন",
    "car": "কার",
    "bike": "বাইক",
    "rickshaw": "রিকশা",
    "road": "রোড",
    "traffic": "ট্রাফিক",
    "police": "পুলিশ",
    "doctor": "ডাক্তার",
    "hospital": "হসপিটাল",
    "patient": "পেশেন্ট",
    "medicine": "মেডিসিন",
    "tablet": "ট্যাবলেট",
    "capsule": "ক্যাপসুল",
    "injection": "ইনজেকশন",
    "test": "টেস্ট",
    "report": "রিপোর্ট",
    "result": "রেজাল্ট",
    "exam": "এক্সাম",
    "class": "ক্লাস",
    "sir": "স্যার",
    "madam": "ম্যাডাম",
    "teacher": "টিচার",
    "student": "স্টুডেন্ট",
    "study": "স্টাডি",
    "book": "বুক",
    "pen": "পেন",
    "paper": "পেপার",
    "file": "ফাইল",
    "bag": "ব্যাগ",
    "lunch": "লাঞ্চ",
    "dinner": "ডিনার",
    "breakfast": "ব্রেকফাস্ট",
    "food": "ফুড",
    "water": "ওয়াটার",
    "tea": "চা",
    "coffee": "কফি",
    "rice": "রাইস",
    "biryani": "বিরিয়ানি",
    "burger": "বার্গার",
    "pizza": "পিৎজা",
    "chicken": "চিকেন",
    "beef": "বিফ",
    "mutton": "মাটন",
    "fish": "ফিশ",
    "egg": "এগ",
    
    # Emotions/Abstract
    "happy": "হ্যাপি",
    "sad": "স্যাড",
    "angry": "অ্যাংরি",
    "excited": "এক্সাইটেড",
    "bored": "বোরড",
    "tired": "টায়ার্ড",
    "busy": "বিজি",
    "free": "ফ্রি",
    "ready": "রেডি",
    "sure": "শিওর",
    "maybe": "মেবি",
    "problem": "প্রবলেম",
    "solution": "সলিউশন",
    "idea": "আইডিয়া",
    "plan": "প্ল্যান",
    "change": "চেঞ্জ",
    "system": "সিস্টেম",
    "style": "স্টাইল",
    "fashion": "ফ্যাশন",
    "model": "মডেল",
    "hero": "হিরো",
    "star": "স্টার",
    "super": "সুপার",
    "hit": "হিট",
    "flop": "ফ্লপ",
    
    # Time
    "time": "টাইম",
    "minute": "মিনিট",
    "hour": "আওয়ার",
    "second": "সেকেন্ড",
    "day": "ডে",
    "week": "উইক",
    "month": "মান্থ",
    "year": "ইয়ার",
    "date": "ডেট",
    "today": "টুডে",
    "tomorrow": "টুমরো",
    "yesterday": "ইয়েস্টারডে",
    "night": "নাইট",
    "morning": "মর্নিং",
    
    # Misc
    "room": "রুম",
    "bed": "বেড",
    "chair": "চেয়ার",
    "table": "টেবিল",
    "fan": "ফ্যান",
    "light": "লাইট",
    "tv": "টিভি",
    "remote": "রিমোট",
    "fridge": "ফ্রিজ",
    "ac": "এসি",
    "laptop": "ল্যাপটপ",
    "computer": "কম্পিউটার",
    "game": "গেম",
    "play": "প্লে",
    "player": "প্লেয়ার",
    "team": "টিম",
    "captain": "ক্যাপ্টেন",
    "goal": "গোল",
    "run": "রান",
    "out": "আউট",
    "ball": "বল",
    "bat": "ব্যাট",
    "six": "সিক্স",
    "four": "ফোর",
    "wicket": "উইকেট",
    "catch": "ক্যাচ",
    "match": "ম্যাচ"
}

def expand_dictionary():
    try:
        with open(DICT_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Dictionary not found!")
        return

    # Normalize keys to lowercase just in case
    # And handle duplication removal by overwriting
    original_count = len(data)
    
    # Merge new words
    for k, v in new_words.items():
        data[k.lower()] = v
        
    # Optional: Fix any existing duplicates logic (already done by python dictionary structure)
    
    final_count = len(data)
    print(f"Original entries: {original_count}")
    print(f"Final entries: {final_count}")
    
    # Write back sorted
    with open(DICT_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)
    
    print("Dictionary successfully expanded and sorted.")

if __name__ == "__main__":
    expand_dictionary()
