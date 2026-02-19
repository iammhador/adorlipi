import json
import os

class PhoneticParser:
    def __init__(self, mapping_path):
        self.mapping_path = mapping_path
        self.vowels = {}
        self.consonants = {}
        self.kars = {}
        self.max_key_len = 0
        self._load_mapping()

    def _load_mapping(self):
        try:
            with open(self.mapping_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.vowels = data.get("vowels", {})
                self.consonants = data.get("consonants", {})
                self.kars = data.get("kars", {})
                
                # Pre-calculate max key length for greedy matching
                all_keys = list(self.vowels.keys()) + list(self.consonants.keys()) + list(self.kars.keys())
                if all_keys:
                    self.max_key_len = max(len(k) for k in all_keys)
                else:
                    self.max_key_len = 1
        except FileNotFoundError:
            print(f"Error: Mapping file not found at {self.mapping_path}")

    def parse(self, word):
        """
        Transliterates a single word using greedy left-to-right parsing.
        """
        i = 0
        n = len(word)
        output = []
        last_was_consonant = False
        
        while i < n:
            match_found = False
            # Try matching patterns from longest to shortest
            for length in range(self.max_key_len, 0, -1):
                if i + length > n:
                    continue
                
                chunk = word[i:i+length]
                # Try exact match first (case sensitive logic if needed, but dict is mostly lowercase)
                # Our mapping is mostly lowercase, but has some caps (T, D). 
                # Word coming in might be normalized or not. 
                # Normalizer lowercases everything? 
                # Wait, normalizer.py lowercases everything. 'word = word.lower()'.
                # So if mapping depends on 'T' vs 't', normalizer destroys that info?
                # The normalizer task said: "Lowercase everything".
                # But mapping needs T vs t distinctions for Twb vs Tob? 
                # Usually in Banglish, `t` implies `ত`. `T` is rare or used for `ট`. 
                # If input is already lowercased, we can't distinguish.
                # However, the user requirement for normalizer said: "Lowercase everything".
                # So we must assume case insensitivity.
                # If so, 't' and 'T' are the same.
                # I will stick to 't' -> 'ত' per user requirement.
                # And 'd' -> 'দ'.
                # If user types 'T', normalizer makes it 't', maps to 'ত'.
                # That's acceptable for MVP of "casual social media Banglish".
                
                lower_chunk = chunk
                
                # Priority: Consonants > Vowels/Kars (usually disjoint sets, but good to order)
                
                # Check Consonants
                if lower_chunk in self.consonants:
                    # Robustness: Fola Handling (Ra-fola, Ya-fola)
                    # If this consonant follows another consonant (no vowel in between), check for special cluster rules.
                    
                    # Ra-fola (Consonant + r -> C + ◌্র)
                    if last_was_consonant and lower_chunk == 'r':
                        # Append Virama + Ra (\u09cd + \u09b0) to form ◌্র
                        # But wait, we want to modify the output, not just append.
                        # Output already has the previous consonant.
                        # So we append the fola.
                        fola = "\u09cd\u09b0"
                        output.append(fola)
                        i += length
                        last_was_consonant = True # Cluster continues
                        match_found = True
                        break

                    # Ya-fola (Consonant + y/z -> C + ◌্য)
                    # User requested 'zfola' -> likely means 'z' triggers ya-fola after consonant
                    elif last_was_consonant and (lower_chunk == 'y' or lower_chunk == 'z'):
                        # Append Virama + Ya (\u09cd + \u09af) to form ◌্য
                        fola = "\u09cd\u09af"
                        output.append(fola)
                        i += length
                        last_was_consonant = True # Cluster continues
                        match_found = True
                        break
                    
                    # Normal Consonant Mapping
                    val = self.consonants[lower_chunk]
                    
                    # If last was consonant, usually imply implicit 'o' or virama?
                    # But in this parser, we just append consonants side-by-side. 
                    # Default rendering handles them as separate letters.
                    # 'k' + 'k' -> 'কক'. 
                    # If we want conjunctions (juktakkharr), that's complex logic (requires dictionary of valid conjuncts).
                    # For now, sticking to Fola support as requested.
                    
                    output.append(val)
                    i += length
                    last_was_consonant = True
                    match_found = True
                    break
                
                # Check Vowels
                if lower_chunk in self.vowels:
                    # If after consonant -> use Kar
                    if last_was_consonant:
                        kar = self.kars.get(lower_chunk)
                        if kar is not None:
                            output.append(kar)
                            # Kar is attached to consonant, now we are "open" or "neutral"?
                            # Usually subsequent vowel means new syllable? 
                            # 'bhai' -> bh + a + i. 
                            # 'bh' -> ভ (cons). last=True.
                            # 'a' -> kar '' (implicit). output ভ. last=True??
                            # If I set last=False, then 'i' becomes independent 'ই'.
                            # 'ভাই' -> 'ভা' + 'ই'. Correct. 
                            # 'bha' -> 'ভা'. 'i' -> 'ই'.
                            # What if 'bhai' -> 'ভই'? No. 
                            # what about 'ki' -> k + i(kar).
                            # 'k' -> 'ক'. last=True.
                            # 'i' -> 'ি'. Output 'কি'. last=False (usually).
                            
                            # Let's say: Kars terminate the consonant syllable. Next vowel is independent.
                            last_was_consonant = False 
                        else:
                             # Fallback if no kar defined (shouldn't happen if vowels mirrored in kars)
                             output.append(self.vowels[lower_chunk])
                             last_was_consonant = False
                    else:
                        # Start of word or after another vowel -> Independent Vowel
                        output.append(self.vowels[lower_chunk])
                        last_was_consonant = False
                        
                    i += length
                    match_found = True
                    break
            
            if match_found:
                continue
            
            # No match handling
            # If no match, just append the character as is? 
            # Or skip? User said "Preserve punctuation" but that's handled by tokenizer.
            # This is inside a word.
            # E.g. "x" not in mapping.
            output.append(word[i])
            i += 1
            last_was_consonant = False  # Reset on unknown
            
        return "".join(output)
