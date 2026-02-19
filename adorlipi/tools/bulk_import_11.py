import json
import os

DICT_PATH = "../data/dictionary.json"

# Phase 11: Administrative Divisions (Zila, Upazila/Thana) & Essentials (Animals, Veg, Food)
bulk_data_11 = {
    # --- 64 Districts (Zila) ---
    "bagerhat": "বাগেরহাট", "bandarban": "বান্দরবান", "barguna": "বরগুনা", "barisal": "বরিশাল",
    "bhola": "ভোলা", "bogra": "বগুড়া", "brahmanbaria": "ব্রাহ্মণবাড়িয়া", "chandpur": "চাঁদপুর",
    "chapainawabganj": "চাপাইনবাবগঞ্জ", "chittagong": "চট্টগ্রাম", "chuadanga": "চুয়াডাঙ্গা",
    "comilla": "কুমিল্লা", "coxsbazar": "কক্সবাজার", "dhaka": "ঢাকা", "dinajpur": "দিনাজপুর",
    "faridpur": "ফরিদপুর", "feni": "ফেনী", "gaibandha": "গাইবান্ধা", "gazipur": "গাজীপুর",
    "gopalganj": "গোপালগঞ্জ", "habiganj": "হবিগঞ্জ", "jamalpur": "জামালপুর", "jessore": "যশোর",
    "jhalokati": "ঝালকাঠি", "jhenaidah": "ঝিনাইদহ", "joypurhat": "জয়পুরহাট", "khagrachari": "খাগড়াছড়ি",
    "khulna": "খুলনা", "kishoreganj": "কিশোরগঞ্জ", "kurigram": "কুড়িগ্রাম", "kushtia": "কুষ্টিয়া",
    "lakshmipur": "লক্ষ্মীপুর", "lalmonirhat": "লালমনিরহাট", "madaripur": "মাদারীপুর", "magura": "মাগুরা",
    "manikganj": "মানিকগঞ্জ", "meherpur": "মেহেরপুর", "moulvibazar": "মৌলভীবাজার", "munshiganj": "মুন্সীগঞ্জ",
    "mymensingh": "ময়মনসিংহ", "naogaon": "নওগাঁ", "narail": "নড়াইল", "narayanganj": "নারায়ণগঞ্জ",
    "narsingdi": "নরসিংদী", "natore": "নাটোর", "netrokona": "নেত্রকোনা", "nilphamari": "নীলফামারী",
    "noakhali": "নোয়াখালী", "pabna": "পাবনা", "panchagarh": "পঞ্চগড়", "patuakhali": "পটুয়াখালী",
    "pirojpur": "পিরোজপুর", "rajbari": "রাজবাড়ী", "rajshahi": "রাজশাহী", "rangamati": "রাঙামাটি",
    "rangpur": "রংপুর", "satkhira": "সাতক্ষীরা", "shariatpur": "শরীয়তপুর", "sherpur": "শেরপুর",
    "sirajganj": "সিরাজগঞ্জ", "sunamganj": "সুনামগঞ্জ", "sylhet": "সিলেট", "tangail": "টাঙ্গাইল",
    "thakurgaon": "ঠাকুরগাঁও",

    # --- Major Thanas / Upazilas / Areas ---
    "mirpur": "মিরপুর", "gulshan": "গুলশান", "banani": "বনানী", "dhanmondi": "ধানমন্ডি",
    "motijheel": "মতিঝিল", "uttara": "উত্তরা", "mohammadpur": "মোহাম্মদপুর", "badda": "বাড্ডা",
    "ramna": "রমনা", "shahbag": "শাহবাগ", "palton": "পল্টন", "khilgaon": "খিলগাঁও",
    "basabo": "বাসাবো", "mugda": "মুগদা", "shyamoli": "শ্যামলী", "adabor": "আদাবর",
    "keraniganj": "কেরানীগঞ্জ", "savar": "সাভার", "ashulia": "আশুলিয়া", "dhamrai": "ধামরাই",
    "nawabganj": "নবাবগঞ্জ", "dohar": "দোহার", "tongi": "টঙ্গী", "kaliganj": "কালীগঞ্জ",
    "kapasia": "কাপাসিয়া", "sreepur": "শ্রীপুর", "kaliakair": "কালিয়াকৈর",
    "sonargaon": "সোনারগাঁও", "rupganj": "রূপগঞ্জ", "araijazar": "আড়াইহাজার",
    "siddhirganj": "সিদ্ধিরগঞ্জ", "fatullah": "ফতুল্লা",
    "shibpur": "শিবপুর", "monohardi": "মনোহরদী", "belabo": "বেলাব", "raipura": "রায়পুরা",
    "lohagara": "লোহাগড়া", "sitakunda": "সীতাকুণ্ড", "mirsharai": "মীরসরাই", "potiya": "পটিয়া",
    "anwara": "আনোয়ারা", "banshkhali": "বাঁশখালী", "boalkhali": "বোয়ালখালী", "chandanaish": "চন্দনাইশ",
    "fatikchhari": "ফটিকছড়ি", "hathazari": "হাটহাজারী", "rangunia": "রাঙ্গুনিয়া", "raoazan": "রাউজান",
    "sandwip": "সন্দ্বীপ", "satkania": "সাতকানিয়া",
    "kotwali": "কোতোয়ালী", "panchlaish": "পাঁচলাইশ", "bayazid": "বায়জিদ", "chandgaon": "চান্দগাঁও",
    "pahartali": "পাহাড়তলী", "halishahar": "হালিশহর", "patenga": "পতেঙ্গা",
    "sadar": "সদর", "biswanath": "বিশ্বনাথ", "beanibazar": "বিয়ানীবাজার", "golapganj": "গোলাপগঞ্জ",
    "fenchuganj": "ফেঞ্চুগঞ্জ", "balaganj": "বালাগঞ্জ", "zakiganj": "জকিগঞ্জ",
    "daudkandi": "দাউদকান্দি", "burichang": "বুড়িচং", "chandina": "চান্দিনা", "homna": "হোমনা",
    "laksham": "লাকসাম", "muradnagar": "মুরাদনগর", "nangalkot": "নাঙ্গলকোট",
    "begumganj": "বেগমগঞ্জ", "chatkhil": "চাটখিল", "senbug": "সেনবাগ", "hatiya": "হাতিয়া",
    "dagonbhuiyan": "দাগনভূঞা", "chhagolnaiya": "ছাগলনাইয়া", "parshuram": "পরশুরাম", "sonagazi": "সোনাগাজী",
    "bheramara": "ভেড়ামারা", "daulatpur": "দৌলতপুর", "khoksa": "খোকসা", "kumarkhali": "কুমারখালী",

    # --- Animals (Expanded) ---
    "tiger": "বাঘ", "lion": "সিংহ", "elephant": "হাতি", "deer": "হরিণ", "monkey": "বানর",
    "cow": "গরু", "goat": "ছাগল", "sheep": "ভেড়া", "dog": "কুকুর", "cat": "বিড়াল",
    "horse": "ঘোড়া", "donkey": "গাধা", "camel": "উট", "buffalo": "মহিষ", "pig": "শূকর",
    "rabbit": "খরগোশ", "mouse": "ইঁদুর", "rat": "ইঁদুর", "squirrel": "কাঠবিড়ালি",
    "fox": "শিয়াল", "bear": "ভালুক", "wolf": "নেকড়ে", "crocodile": "কুমির", "snake": "সাপ",
    "frog": "ব্যাঙ", "turtle": "কচ্ছপ", "lizard": "টিকটিকি",
    "bird": "পাখি", "crow": "কাক", "pigeon": "কবুতর", "sparrow": "চড়ুই", "parrot": "টিয়া",
    "eagle": "ঈগল", "owl": "প্যাঁচা", "peacock": "ময়ূর", "swan": "রাজহাঁস", "duck": "হাঁস",
    "hen": "মুরগি", "cock": "মোরগ", "chicken": "মুরগি",
    "fish": "মাছ", "hilsha": "ইলিশ", "ruhi": "রুই", "katla": "কাতলা", "shrimp": "চিংড়ি",
    "prawn": "চিংড়ি", "crab": "কাঁকড়া", "shark": "হাঙর", "dolphin": "ডলফিন", "whale": "তিমি",
    "fly": "মাছি", "mosquito": "মশা", "ant": "পিঁপড়া", "bee": "মৌমাছি", "butterfly": "প্রজাপতি",
    "spider": "মাকড়সা", "cockroach": "তেলাপোকা",

    # --- Vegetables (Expanded) ---
    "potato": "আলু", "tomato": "টমেটো", "onion": "পেঁয়াজ", "garlic": "রসুন", "ginger": "আদা",
    "chili": "মরিচ", "green chili": "কাঁচা মরিচ", "red chili": "শুকনা মরিচ",
    "cucumber": "শসা", "carrot": "গাজর", "radish": "মুলা", "eggplant": "বেগুন", "brinjal": "বেগুন",
    "cauliflower": "ফুলকপি", "cabbage": "বাঁধাকপি", "spinach": "পালং শাক", "pumpkin": "মিষ্টিকুমড়া",
    "gourd": "লাউ", "bottle gourd": "লাউ", "lady finger": "ঢেঁড়স", "okra": "ঢেঁড়স",
    "bean": "শিম", "pea": "মটরশুঁটি", "lemon": "লেবু", "coriander": "ধনে পাতা",
    "mint": "পুদিনা", "turmeric": "হলুদ", "cumin": "জিরা", "black pepper": "গোলমরিচ",
    "cinnamon": "দারুচিনি", "cardamom": "এলাচ", "clove": "লবঙ্গ",

    # --- Fruits (Expanded) ---
    "apple": "আপেল", "banana": "কলা", "orange": "কমলা", "grape": "আঙ্গুর", "mango": "আম",
    "jackfruit": "কাঁঠাল", "guava": "পেয়ারা", "pineapple": "আনারস", "papaya": "পেঁপে",
    "watermelon": "তরমুজ", "melon": "বাঙ্গি", "pomegranate": "ডালিম", "lemon": "লেবু",
    "lime": "লেবু", "coconut": "নারকেল", "date": "খেজুর", "berry": "জাম",
    "strawberry": "স্ট্রবেরি", "litchi": "লিচু", "lichee": "লিচু", "pear": "নাশপাতি",

    # --- Foods (Expanded) ---
    "rice": "ভাত", "boiled rice": "ভাত", "puffed rice": "মুড়ি", "flattened rice": "চিড়া",
    "bread": "রুটি", "curry": "তরকারি", "dal": "ডাল", "pulse": "ডাল",
    "meat": "মাংস", "beef": "গরুর মাংস", "mutton": "খাসির মাংস", "chicken curry": "মুরগির মাংস",
    "fish curry": "মাছের তরকারি", "egg": "ডিম", "omlette": "মামলেট", "fry": "ভাজি",
    "milk": "দুধ", "curd": "দই", "yogurt": "দই", "butter": "মাখন", "ghee": "ঘি",
    "cheese": "পনির", "oil": "তেল", "sugar": "চিনি", "salt": "লবণ",
    "water": "পানি", "tea": "চা", "coffee": "কফি", "juice": "জুস",
    "sweet": "মিষ্টি", "cake": "কেক", "biscuit": "বিস্কুট", "sweets": "মিষ্টি",
    "honey": "মধু", "pickle": "আচার", "sauce": "সস", "jam": "জ্যাম", "jelly": "জেলি",
    "polao": "পোলাও", "biryani": "বিরিয়ানি", "khichuri": "খিচুড়ি", "tehari": "তেহারি",
    "fuchka": "ফুচকা", "chotpoti": "চটপটি", "samosa": "সিঙাড়া", "singara": "সিঙাড়া",
    "puri": "পুরি", "chop": "চপ", "kebab": "কাবাব", "paratha": "পরোটা",
    "breakfast": "সকালের নাস্তা", "lunch": "দুপুরের খাবার", "dinner": "রাতের খাবার",
    "snack": "নাস্তা", "feast": "ভোজ",
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
    
    # Process Phase 11
    print("\nProcessing Bulk Import Phase 11 (Administrative & Essentials)...")
    for eng, bng in bulk_data_11.items():
        eng_lower = eng.lower().strip()
        if eng_lower not in current_dict:
            current_dict[eng_lower] = bng
            added_count += 1
        else:
            skipped_count += 1
            # Optional: Overwrite if you trust this list more? 
            # For now, let's keep existing if present, but some might be better here.
            # actually for administrative, let's ensure they are correct (often phonetic before)
            # but usually first valid entry is fine.
            
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
