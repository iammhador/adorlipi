import json
import os

new_slang = {
    "vau": "ভাই",
    "corporate": "কর্পোরেট",
    "wp": "হোয়াটসঅ্যাপ",
    "nije": "নিজে",
    "beda": "ব্যাটা",
    "afsos": "আফসোস",
    "kacha": "কাঁচা",
    "baad": "বাদ",
    "aisha": "আইসা",
    "edi": "এডি",
    "purada": "পুরাটা",
    "mnt": "মিনিট",
    "koise": "কইছে",
    "kaam": "কাম",
    "poiraa": "পইড়া",
    "koiraa": "কইরা",
    "dhon": "ধন",
    "oidar": "ঐডার",
    "jonman": "জন্মাইতে",
    "lagboo": "লাগবো",
    "amre": "আমারে",
    "koili": "কইলি",
    "fascination": "ফ্যাসিনেশন",
    "or": "ওর"
}

with open("data/dictionary.json", "r", encoding="utf-8") as f:
    d = json.load(f)

for k, v in new_slang.items():
    d[k] = v

with open("data/dictionary.json", "w", encoding="utf-8") as f:
    json.dump(dict(sorted(d.items())), f, ensure_ascii=False, indent=4)
    
with open("docs/data/dictionary.json", "w", encoding="utf-8") as f:
    json.dump(dict(sorted(d.items())), f, ensure_ascii=False, indent=4)

print("Injected extreme slang and abbreviations successfully!")
