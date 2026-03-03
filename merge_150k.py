import pyavrophonetic
import os
import json

config_dir = os.path.dirname(pyavrophonetic.__file__)
print(os.listdir(config_dir))

for f in os.listdir(config_dir):
    if f.endswith('.json'):
        path = os.path.join(config_dir, f)
        print("Found dict:", path)
        with open("data/dictionary.json", "r", encoding="utf-8") as dic_f:
            ador_dict = json.load(dic_f)
            
        with open(path, "r", encoding="utf-8") as ext_f:
            avro_data = json.load(ext_f)
            
        if 'words' in avro_data:
            avro_data = avro_data['words']
            
        mapping = {}
        if isinstance(avro_data, list):
            for obj in avro_data:
                if 'word' in obj and 'replace' in obj:
                    mapping[obj['word']] = obj['replace']
        elif isinstance(avro_data, dict):
            mapping = avro_data
            
        print("Extracted", len(mapping), "records.")
        
        original_len = len(ador_dict)
        added_count = 0
        for k, v in mapping.items():
             k_lower = k.lower()
             if k_lower not in ador_dict and " " not in k_lower and len(k_lower) > 1:
                  ador_dict[k_lower] = v
                  added_count += 1
                  
        sorted_dict = dict(sorted(ador_dict.items()))
        with open("data/dictionary.json", "w", encoding='utf-8') as out_f:
             json.dump(sorted_dict, out_f, ensure_ascii=False, indent=4)
             
        print(f"BUMPED DICTIONARY FROM {original_len} to {len(sorted_dict)}! Added {added_count} words natively.")
