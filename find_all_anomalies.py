import json
import os
import sys
import difflib

sys.path.insert(0, os.path.abspath('/home/onism/LOG FILE/__ ADOR __'))
from core.engine.transliterator import Transliterator

dict_path = "/home/onism/LOG FILE/__ ADOR __/data/dictionary.json"

with open(dict_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

engine = Transliterator()

anomalies = []

# Safe Banglish whitelisted words that we know differ phonetically but are valid
whitelist = {'allah', 'bismillah', 'muhammad', 'alhamdulillah'}

for banglish, dict_bangla in data.items():
    if len(banglish) < 4 or banglish.lower() in whitelist:
        continue
        
    engine_bangla = engine.transliterate(banglish.lower())
    
    # Calculate similarity between dictionary spelling and machine spelling
    ratio = difflib.SequenceMatcher(None, dict_bangla, engine_bangla).ratio()
    
    # If the dictionary spelling shares less than 30% of its Bengali characters
    # with the expected phonetic spelling, it's highly suspect! 
    # (Probably a semantic translation or a massive typo).
    if ratio < 0.35:
        anomalies.append({
            "banglish": banglish,
            "dict_value": dict_bangla,
            "engine_value": engine_bangla,
            "ratio": ratio
        })

print(f"Scanned {len(data)} words. Found {len(anomalies)} extreme phonetic anomalies (Ratio < 0.35).")

# Sort anomalies from worst (0.0 ratio) to slightly better (0.35 ratio)
anomalies.sort(key=lambda x: x['ratio'])

print("\n--- TOP SUSPECTED TRANSLATIONS / ANOMALIES ---")
for i, anomaly in enumerate(anomalies):
    if i >= 50:
        break
    print(f"[{anomaly['ratio']:.2f}] {anomaly['banglish']} -> Dict mapping: {anomaly['dict_value']} | Expected Phonetic: {anomaly['engine_value']}")
