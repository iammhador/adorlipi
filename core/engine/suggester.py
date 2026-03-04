import os
import json

class Suggester:
    # Phonetic ambiguity map: characters that sound similar in Banglish
    AMBIGUOUS = {
        'ত': ['ট', 'থ', 'ঠ'],
        'ট': ['ত', 'ঠ', 'থ'],
        'দ': ['ড', 'ধ', 'ঢ'],
        'ড': ['দ', 'ঢ', 'ধ'],
        'ধ': ['দ', 'ড', 'ঢ'],
        'ঢ': ['ড', 'দ', 'ধ'],
        'থ': ['ত', 'ট', 'ঠ'],
        'ঠ': ['ট', 'ত', 'থ'],
        'স': ['শ', 'ষ'],
        'শ': ['স', 'ষ'],
        'ষ': ['স', 'শ'],
        'ন': ['ণ'],
        'ণ': ['ন'],
        'র': ['ড়', 'ঢ়'],
        'ড়': ['র', 'ঢ়'],
        'ঢ়': ['ড়', 'র'],
        'জ': ['য', 'ঝ'],
        'য': ['জ'],
        'ঝ': ['জ'],
        'ই': ['ঈ'],
        'ঈ': ['ই'],
        'উ': ['ঊ'],
        'ঊ': ['উ'],
        'ি': ['ী'],
        'ী': ['ি'],
        'ু': ['ূ'],
        'ূ': ['u'],
        'ো': ['ো'],
        'ে': ['ৈ'],
    }

    def __init__(self, data_path=None):
        if data_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            data_path = os.path.join(base_dir, 'data', 'openbangla_dictionary.json')

        self.word_pool = []
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Pre-flatten into a single sorted list for O(n) scanning
                seen = set()
                for arr in data.values():
                    for w in arr:
                        if w not in seen:
                            self.word_pool.append(w)
                            seen.add(w)
        except Exception as e:
            print(f"Warning: Failed to load dictionary: {e}")

    def _generate_variants(self, target):
        """
        Deep ambiguity: generate alternate Bangla strings by replacing
        EACH ambiguous character (not just the first one).
        Returns a list of variant strings including the original.
        """
        variants = [target]

        # Scan every character position for ambiguity
        for i, ch in enumerate(target):
            if ch in self.AMBIGUOUS:
                new_variants = []
                for v in variants:
                    for alt in self.AMBIGUOUS[ch]:
                        new_variants.append(v[:i] + alt + v[i+1:])
                variants.extend(new_variants)

        # Deduplicate while preserving order (original first)
        seen = set()
        unique = []
        for v in variants:
            if v not in seen:
                seen.add(v)
                unique.append(v)
        return unique

    def get_suggestions(self, buffer, target_bangla):
        """
        Production-grade suggestion engine.
        1. Generates deep phonetic variants of target_bangla.
        2. Scans the full 150k word pool.
        3. Ranks: exact-prefix first, then ambiguous-prefix, shortest first.
        """
        if not buffer or not target_bangla or not self.word_pool:
            return []

        search_targets = self._generate_variants(target_bangla)
        primary = target_bangla  # The exact transliteration

        exact_matches = []    # Words starting with the exact transliteration
        fuzzy_matches = []    # Words starting with an ambiguous variant

        for word in self.word_pool:
            if word == target_bangla:
                continue  # Skip the exact same word

            # Check exact prefix first (highest priority)
            if word.startswith(primary):
                exact_matches.append(word)
                if len(exact_matches) >= 15:
                    continue

            # Check ambiguous variant prefixes
            for alt in search_targets[1:]:  # Skip primary (already checked)
                if word.startswith(alt) and word != alt:
                    fuzzy_matches.append(word)
                    break

            if len(exact_matches) + len(fuzzy_matches) >= 40:
                break

        # Sort each bucket by length (shorter = more common/useful)
        exact_matches.sort(key=len)
        fuzzy_matches.sort(key=len)

        # Merge: exact matches first, then fuzzy
        combined = []
        seen = set()
        for w in exact_matches + fuzzy_matches:
            if w not in seen:
                seen.add(w)
                combined.append(w)
            if len(combined) >= 5:
                break

        return combined
