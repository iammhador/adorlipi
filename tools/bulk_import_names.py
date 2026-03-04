import json
import os

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dict_path = os.path.join(base_dir, 'data', 'dictionary.json')
    openbangla_path = os.path.join(base_dir, 'data', 'openbangla_dictionary.json')

    dictionary = load_json(dict_path)
    openbangla = load_json(openbangla_path)

    print(f"Current core dictionary size: {len(dictionary)}")

    # Specific common Muslim and Bengali names with confusing consonant clusters
    names_to_add = {
        # R-fola overrides
        'kamrul': 'কামরুল',
        'qamrul': 'কামরুল',
        'jamrul': 'জামরুল',
        'amrul': 'আমরুল',
        'imrul': 'ইমরুল',
        'fakhrul': 'ফখরুল',
        'tajrul': 'তাজরুল',
        'nazrul': 'নজরুল',
        'badrul': 'বদরুল',
        'bodrul': 'বদরুল',
        'amirul': 'আমিরুল',
        'johurul': 'জহুরুল',
        'zahurul': 'জহুরুল',
        'zohurul': 'জহুরুল',
        'aminul': 'আমিনুল',
        'mominul': 'মুমিনুল',
        'mofizul': 'মফিজুল',
        'mafizul': 'মাফিজুল',
        'khairul': 'খাইরুল',
        'sirajul': 'সিরাজুল',
        'shariful': 'শরিফুল',
        'soriful': 'শরিফুল',
        'tariqul': 'তরিকুল',
        'torikul': 'তরিকুল',
        'rafiqul': 'রফিকুল',
        'rofikul': 'রফিকুল',
        'shofiqul': 'শফিকুল',
        'shafiqul': 'শফিকুল',
        'ariful': 'আরিফুল',
        'samrat': 'সম্রাট',
        'shamrat': 'সম্রাট',
        'imroj': 'ইমরোজ',
        'numan': 'নুমান',
        'noman': 'নোমান',
        'rabbi': 'রাব্বি',
        'robbi': 'রাব্বি',
        'robbin': 'রবিন',
        'robin': 'রবিন',
        'rakib': 'রাকিব',
        'rokib': 'রকিব',
        'shakil': 'শাকিল',
        'sokil': 'সাকিল',
        'jamal': 'জামাল',
        'kamal': 'কামাল',
        'ashraful': 'আশরাফুল',
        'mohammad': 'মোহাম্মদ',
        'muhammad': 'মুহাম্মদ',
        'mahmud': 'মাহমুদ',
        'hasan': 'হাসান',
        'hossain': 'হোসেন',
        'husain': 'হুসাইন',
        'rahman': 'রহমান',
        'rohman': 'রহমান',
        'ahmed': 'আহমেদ',
        'ahamed': 'আহমেদ',
        'sohel': 'সোহেল',
        'rubel': 'রুবেল',
        'rasel': 'রাসেল',
        'alam': 'আলম',
        'islam': 'ইসলাম',
        'kholil': 'খলিল',
        'khalil': 'খলিল',
        'jalil': 'জলিল',
        'jolil': 'জলিল',
        'habib': 'হাবিব'
    }

    count = 0
    for key, val in names_to_add.items():
        if key not in dictionary:
            dictionary[key] = val
            count += 1

    save_json(dict_path, dictionary)
    print(f"Added {count} common name exceptions.")
    print(f"New core dictionary size: {len(dictionary)}")

if __name__ == "__main__":
    main()
