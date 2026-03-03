import json
import urllib.request
import os

print("Fetching Massive 150k Bengali Dictionary (Avro/OpenBangla format)...")

# OpenBangla/Avro usually structures dictionaries as {"banglish": "bangla"} or lists of objects
# We will use the widely available bangla-dictionary JSON from mugli or pyavro as a massive source
URL = "https://raw.githubusercontent.com/mugli/inexact-search/master/bangla-dictionary.json"
# Fallback if that URL isn't 150k, we can use the main Avro dict. 
# Many open source projects host the Avro dictionary as a JSON file.
# Let's try downloading the 90k-150k words JSON commonly used in JS/Python phonetic engines.

try:
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        external_data = json.loads(response.read().decode())
    print(f"✅ Fetched {len(external_data)} words successfully.")
except Exception as e:
    print("Failed to fetch primary URL, trying alternative source...", e)
    # Give a known massive dictionary if first fails
    ALT_URL = "https://raw.githubusercontent.com/shantanuo/spell_checker/master/bengali_dictionary.txt"
    try:
        req = urllib.request.Request(ALT_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            external_data = {}
            lines = response.read().decode().splitlines()
            for line in lines:
                external_data[line.strip()] = line.strip() # This is just Bengali words, not a mapping!
        print(f"✅ Fetched {len(external_data)} words successfully.")
    except Exception as e2:
         print("Failed", e2)
         exit(1)

# Oh wait, if the source is JUST bengali words (like the second one), we'd need to reverse-engineer phonetics.
# Let's see what the first URL returns.
