import json
import os
import logging

class PhoneticParser:
    def __init__(self, mapping_path, conjunct_map_path=None, overrides_path=None):
        self.mapping_path = mapping_path
        self.conjunct_map_path = conjunct_map_path
        self.overrides_path = overrides_path
        self.vowels = {}
        self.consonants = {}
        self.kars = {}
        self.folas = {}
        self.inspired_conjuncts = {}
        self.word_overrides = {}
        self.max_key_len = 0
        self._load_mapping()
        self._load_conjunct_map()
        self._load_word_overrides()

    def _load_mapping(self):
        try:
            with open(self.mapping_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.vowels = data.get("vowels", {})
                self.consonants = data.get("consonants", {})
                self.kars = data.get("kars", {})
                self.folas = data.get("folas", {})
                
                # Pre-calculate max key length for greedy matching
                all_keys = list(self.vowels.keys()) + list(self.consonants.keys()) + list(self.kars.keys()) + list(self.folas.keys())
                if all_keys:
                    self.max_key_len = max(len(k) for k in all_keys)
                else:
                    self.max_key_len = 1
        except FileNotFoundError:
            print(f"Error: Mapping file not found at {self.mapping_path}")

    def _load_conjunct_map(self):
        if not self.conjunct_map_path:
            return
        try:
            with open(self.conjunct_map_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            pairs = data.get("pairs", {})
            if isinstance(pairs, dict):
                self.inspired_conjuncts = pairs
        except FileNotFoundError:
            self.inspired_conjuncts = {}

    def _load_word_overrides(self):
        if not self.overrides_path:
            self.overrides_path = os.path.join(
                os.path.dirname(self.mapping_path),
                "phonetic_overrides.json",
            )

        try:
            with open(self.overrides_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    self.word_overrides = {
                        k.lower(): v for k, v in data.items()
                        if isinstance(k, str) and isinstance(v, str)
                    }
        except FileNotFoundError:
            self.word_overrides = {}

    def parse(self, word):
        """
        Transliterates a single word using greedy left-to-right parsing with contextual heuristics.
        """
        override = self.word_overrides.get(word.lower())
        if override:
            return override

        i = 0
        n = len(word)
        output = []
        last_was_consonant = False
        implicit_vowel_dropped = False
        last_parsed_chunk = None
        
        while i < n:
            match_found = False
            for length in range(self.max_key_len, 0, -1):
                if i + length > n:
                    continue
                
                chunk = word[i:i+length]
                lower_chunk = chunk
                
                # Check Fola Triggers FIRST
                if last_was_consonant and lower_chunk in self.folas:
                    fola_val = self.folas[lower_chunk]
                    # Avoid double hasant if the last output already ends with one (e.g., from a Ref)
                    if output and output[-1].endswith("\u09cd") and fola_val.startswith("\u09cd"):
                        output.append(fola_val[1:])
                    else:
                        output.append(fola_val)
                    i += length
                    last_was_consonant = True 
                    implicit_vowel_dropped = False
                    last_parsed_chunk = lower_chunk
                    match_found = True
                    break

                # Double Consonant Rule
                if last_was_consonant and lower_chunk in self.consonants:
                    # Only trigger if the previously parsed explicit consonant chunk EXACTLY matches this one
                    if last_parsed_chunk == lower_chunk and len(lower_chunk) == 1:
                        output.append("\u09cd") # Virama
                        output.append(self.consonants[lower_chunk])
                        i += length
                        last_was_consonant = True
                        implicit_vowel_dropped = False
                        last_parsed_chunk = lower_chunk
                        match_found = True
                        break
                
                # Contextual Ref (◌র্) Rule
                # We only want this to apply if 'r' is NOT acting as a Fola (which means we should only apply it if NOT last_was_consonant)
                # Wait, 'khorgos'. kh + o(drop) -> last_was_consonant=False. Then 'r'. last_was_consonant=False -> NOT Fola.
                # So if 'r' is preceded by a consonant (last_was_consonant=True), it is a Ra-Fola (প্র).
                # Contextual Ref ONLY applies when last_was_consonant = False!
                if not last_was_consonant and lower_chunk == 'r' and i + 1 < n:
                    next_char = word[i+1]
                    if next_char in self.consonants:
                        # Avro-style logic: if preceded by an implicit vowel (like 'kho' in 'khorgos'), 
                        # 'r' does NOT form a Ref. It just becomes 'র'.
                        # We track `implicit_vowel_dropped`. If true, we just map 'r' normally.
                        if not implicit_vowel_dropped:
                            # Forming a Ref
                            output.append("\u09b0\u09cd")
                            i += length
                            last_was_consonant = True 
                            implicit_vowel_dropped = False
                            last_parsed_chunk = lower_chunk
                            match_found = True
                            break

                # Check Consonants
                if lower_chunk in self.consonants:
                    # If we have consecutive consonants, try inspired conjunct rules
                    # only when the pair is not already explicitly handled in mapping.json.
                    if (
                        last_was_consonant
                        and output
                        and last_parsed_chunk in self.consonants
                    ):
                        pair_key = f"{last_parsed_chunk}{lower_chunk}"
                        conjunct_val = self.inspired_conjuncts.get(pair_key)
                        if (
                            conjunct_val
                            and pair_key not in self.consonants
                            and output[-1] == self.consonants[last_parsed_chunk]
                        ):
                            output[-1] = conjunct_val
                            i += length
                            last_was_consonant = True
                            implicit_vowel_dropped = False
                            last_parsed_chunk = pair_key
                            match_found = True
                            break

                    val = self.consonants[lower_chunk]
                    output.append(val)
                    i += length
                    last_was_consonant = True
                    implicit_vowel_dropped = False
                    last_parsed_chunk = lower_chunk
                    match_found = True
                    break
                
                # Check Vowels
                if lower_chunk in self.vowels:
                    is_o = (lower_chunk == 'o' or lower_chunk == 'O')
                    
                    if last_was_consonant:
                        if is_o:
                            drop_o = False
                            # Evaluate if 'o' should be dropped (treated as intrinsic invisible 'অ')
                            if i + length == n:
                                drop_o = False # Always keep trailing 'o' (bhalo)
                                # UNLESS preceded by a conjunct (len > 1 in Bengali)
                                if last_parsed_chunk and last_parsed_chunk in self.consonants:
                                    bn_char = self.consonants[last_parsed_chunk]
                                    # len(bn_char) > 1 catches 'ন্ত', 'ন্দ', 'ক্ষ' etc.
                                    if len(bn_char) > 1:
                                        drop_o = True
                            else:
                                next_chunk = word[i+length:]
                                temp_i = 0
                                cons_count = 0
                                while temp_i < len(next_chunk):
                                    matched = False
                                    for c_len in range(self.max_key_len, 0, -1):
                                        if temp_i + c_len <= len(next_chunk):
                                            chunk_key = next_chunk[temp_i:temp_i+c_len]
                                            if chunk_key in self.consonants:
                                                bn_val = self.consonants[chunk_key]
                                                if len(bn_val) > 1:
                                                    cons_count += 2
                                                else:
                                                    cons_count += 1
                                                temp_i += c_len
                                                matched = True
                                                break
                                    if not matched:
                                        break
                                
                                # If followed by vowel
                                if cons_count == 0:
                                    drop_o = False
                                # If followed by a consonant cluster (e.g., khorgos -> rg) -> drop the first 'o'
                                elif cons_count >= 2:
                                    drop_o = True
                                # If followed by 1 consonant and end of word (e.g., pagol) 
                                elif cons_count == 1 and temp_i == len(next_chunk):
                                    # Heuristic for Banglish verb suffixes ending in -nor or -lor 
                                    # (e.g., ghuchan-o-r -> ঘুছানোর, shamlan-o-r -> শামলানোর)
                                    if last_parsed_chunk in ['n', 'l'] and next_chunk == 'r':
                                        drop_o = False
                                    else:
                                        drop_o = True
                                else:
                                    drop_o = False
                                    
                            if drop_o:
                                implicit_vowel_dropped = True
                                last_was_consonant = False 
                                last_parsed_chunk = None
                            else:
                                kar = self.kars.get(lower_chunk)
                                if kar is not None:
                                    output.append(kar)
                                else:
                                    output.append(self.vowels[lower_chunk])
                                last_was_consonant = False 
                                implicit_vowel_dropped = False
                                last_parsed_chunk = None
                                
                        else: # Not 'o'
                            kar = self.kars.get(lower_chunk)
                            if kar is not None:
                                output.append(kar)
                            else:
                                output.append(self.vowels[lower_chunk])
                            last_was_consonant = False 
                            implicit_vowel_dropped = False
                            last_parsed_chunk = None
                            
                    else:
                        # Independent Vowel
                        output.append(self.vowels[lower_chunk])
                        last_was_consonant = False
                        implicit_vowel_dropped = False
                        last_parsed_chunk = None
                        
                    i += length
                    match_found = True
                    break
            
            if match_found:
                continue
            
            output.append(word[i])
            i += 1
            last_was_consonant = False  
            implicit_vowel_dropped = False
            last_parsed_chunk = None
            
        return "".join(output)
