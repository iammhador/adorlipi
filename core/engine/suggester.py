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
        'ূ': ['ু'],
        'ে': ['ৈ'],
    }

    def __init__(self, data_path=None):
        if data_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            data_path = os.path.join(base_dir, 'data', 'openbangla_dictionary.json')

        self.word_pool = []
        self.word_freq = {}
        self.context_engine = None

        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                seen = set()
                for arr in data.values():
                    for w in arr:
                        if w not in seen:
                            self.word_pool.append(w)
                            seen.add(w)
        except Exception as e:
            print(f"Warning: Failed to load dictionary: {e}")

        # Load frequency data
        freq_path = os.path.join(os.path.dirname(data_path), 'word_frequency.json')
        try:
            with open(freq_path, 'r', encoding='utf-8') as f:
                self.word_freq = json.load(f)
        except Exception:
            pass  # Frequency data is optional, falls back to length-based sorting

    def set_context_engine(self, context_engine):
        """Allows the transliterator to inject the shared context engine."""
        self.context_engine = context_engine

    def _generate_variants(self, target):
        """
        Deep ambiguity: generate alternate Bangla strings by replacing
        EACH ambiguous character (not just the first one).
        Capped at 10 variants to prevent combinatorial explosion.
        """
        variants = [target]

        for i, ch in enumerate(target):
            if ch in self.AMBIGUOUS and len(variants) < 10:
                new_variants = []
                for v in variants:
                    for alt in self.AMBIGUOUS[ch]:
                        new_variants.append(v[:i] + alt + v[i+1:])
                        if len(variants) + len(new_variants) >= 10:
                            break
                    if len(variants) + len(new_variants) >= 10:
                        break
                variants.extend(new_variants)

        seen = set()
        unique = []
        for v in variants:
            if v not in seen:
                seen.add(v)
                unique.append(v)
        return unique

    def _score_word(self, word, is_exact):
        """
        Composite scoring: frequency + context boost + exact-match bonus.
        Higher score = more relevant suggestion.
        """
        score = 0

        # 1. Frequency score (how common is this word in Bengali?)
        score += self.word_freq.get(word, 10)

        # 2. Exact-match bonus (word matched the primary transliteration prefix)
        if is_exact:
            score += 30

        # 3. Context boost from N-gram engine (does it follow the previous word?)
        if self.context_engine:
            score += self.context_engine.score_boost(word)

        # 4. Length penalty for very long words (>8 chars are rarely useful)
        if len(word) > 8:
            score -= (len(word) - 8) * 3

        return score

    def get_suggestions(self, buffer, target_bangla):
        """
        Production-grade suggestion engine with frequency + context ranking.
        1. Generates deep phonetic variants of target_bangla.
        2. Scans the full 150k word pool.
        3. Ranks by composite score: frequency + context + exact-match.
        """
        if not buffer or not target_bangla or not self.word_pool:
            return []

        search_targets = self._generate_variants(target_bangla)
        primary = target_bangla

        candidates = []  # List of (word, score) tuples

        for word in self.word_pool:
            if word == target_bangla:
                continue

            # Check exact prefix
            if word.startswith(primary):
                score = self._score_word(word, is_exact=True)
                candidates.append((word, score))
                continue

            # Check ambiguous variant prefixes
            for alt in search_targets[1:]:
                if word.startswith(alt) and word != alt:
                    score = self._score_word(word, is_exact=False)
                    candidates.append((word, score))
                    break

            if len(candidates) >= 40:
                break

        # Sort by score descending (highest = most relevant)
        candidates.sort(key=lambda x: -x[1])

        # Deduplicate and return top 5
        seen = set()
        result = []
        for word, score in candidates:
            if word not in seen:
                seen.add(word)
                result.append(word)
            if len(result) >= 5:
                break

        return result

