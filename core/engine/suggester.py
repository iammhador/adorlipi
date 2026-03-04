import os
import json

class Suggester:
    def __init__(self, data_path=None):
        if data_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            data_path = os.path.join(base_dir, 'data', 'openbangla_dictionary.json')
        
        self.dict_data = {}
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                self.dict_data = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load openbangla_dictionary.json: {e}")

    def get_suggestions(self, buffer, target_bangla):
        """
        Takes the user's current English buffer (e.g., 'kaj') and the primary transliteration ('কাজ').
        Finds candidate words from the 150k dictionary that start with 'কাজ'.
        """
        if not buffer or not target_bangla or not self.dict_data:
            return []

        # Build search targets based on phonetic ambiguity
        # E.g. If the engine output 'দ', the user might have meant 'ড' or 'ধ'
        # Since capitalization is banned, the Suggester handles the fuzzy logic.
        search_targets = [target_bangla]
        
        ambiguous_starts = {
            'ত': ['ট', 'থ', 'ঠ'],
            'ট': ['ত', 'ঠ', 'থ'],
            'দ': ['ড', 'ধ', 'ঢ'],
            'ড': ['দ', 'ঢ', 'ধ'],
            'স': ['শ', 'ষ'],
            'শ': ['স', 'ষ'],
            'ন': ['ণ'],
            'ণ': ['ন'],
            'র': ['ড়', 'ঢ়'],
            'ড়': ['র', 'ঢ়'],
            'জ': ['য'],
            'য': ['জ'],
            'ই': ['ঈ'],
            'উ': ['ঊ']
        }
        
        first_char = target_bangla[0]
        if first_char in ambiguous_starts:
            # Generate alternate words by replacing the first character
            for alt_char in ambiguous_starts[first_char]:
                alt_target = alt_char + target_bangla[1:]
                search_targets.append(alt_target)

        suggestions = []
        # Python scans all 150k elements in ~10-15ms
        for array in self.dict_data.values():
            for word in array:
                for target in search_targets:
                    if word.startswith(target) and word not in search_targets:
                        suggestions.append(word)
                        break # Move to next word if matched to prevent duplicates
                        
            if len(suggestions) >= 20:
                break
        
        # Sort by length (shortest first) and return top 5
        suggestions.sort(key=len)
        return suggestions[:5]
