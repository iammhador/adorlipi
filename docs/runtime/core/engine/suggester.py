import os
import json
import bisect

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

    def __init__(self, data_path=None, conversational_data_path=None):
        if data_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            data_path = os.path.join(base_dir, 'data', 'openbangla_dictionary.json')
            conversational_data_path = os.path.join(base_dir, 'data', 'dictionary.json')

        if conversational_data_path is None:
            conversational_data_path = os.path.join(os.path.dirname(data_path), 'dictionary.json')

        self.word_pool = []
        self.sorted_word_pool = []
        self.word_freq = {}
        self.context_engine = None
        self.conversational_words = set()
        self.sorted_conversational_words = []

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
        self.sorted_word_pool = sorted(self.word_pool)

        # Load frequency data
        freq_path = os.path.join(os.path.dirname(data_path), 'word_frequency.json')
        try:
            with open(freq_path, 'r', encoding='utf-8') as f:
                self.word_freq = json.load(f)
        except Exception:
            pass  # Frequency data is optional, falls back to length-based sorting

        try:
            with open(conversational_data_path, 'r', encoding='utf-8') as f:
                conv_data = json.load(f)
            if isinstance(conv_data, dict):
                self.conversational_words = {
                    v for v in conv_data.values() if isinstance(v, str) and v
                }
                self.sorted_conversational_words = sorted(self.conversational_words)
        except Exception:
            self.conversational_words = set()
            self.sorted_conversational_words = []

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

        # 1. Frequency score with cap to prevent raw corpora domination.
        freq = self.word_freq.get(word, 10)
        score += min(freq, 120)

        # 2. Exact prefix bonus.
        if is_exact:
            score += 24

        # 3. Conversational dictionary words get a usability boost.
        if word in self.conversational_words:
            score += 16

        # 4. Short-chat friendliness.
        if len(word) <= 6:
            score += (7 - len(word)) * 3

        # 5. Context boost from N-gram engine (does it follow the previous word?)
        if self.context_engine:
            score += self.context_engine.score_boost(word)

        # 6. Length and rarity penalties for overly long obscure candidates.
        if len(word) > 8:
            score -= (len(word) - 8) * 3
        if len(word) > 9 and freq < 30:
            score -= 20

        return score

    def _prefix_candidates_from_pool(self, prefix, pool, limit=300):
        if not prefix or not pool:
            return []

        left = bisect.bisect_left(pool, prefix)
        right = bisect.bisect_right(pool, prefix + "\uffff")
        if left >= right:
            return []
        return pool[left:min(right, left + limit)]

    def _prefix_candidates(self, prefix, limit=300):
        primary = self._prefix_candidates_from_pool(prefix, self.sorted_word_pool, limit=limit)
        conversational = self._prefix_candidates_from_pool(
            prefix,
            self.sorted_conversational_words,
            limit=limit,
        )
        if not conversational:
            return primary
        return primary + conversational

    def get_suggestions(self, buffer, target_bangla):
        """
        Production-grade suggestion engine with frequency + context ranking.
        1. Generates deep phonetic variants of target_bangla.
        2. Collects broad prefix candidates via bisect-range lookup.
        3. Ranks by conversational score profile and context.
        """
        if not buffer or not target_bangla or not self.sorted_word_pool:
            return []

        search_targets = self._generate_variants(target_bangla)
        candidate_flags = {}

        for idx, prefix in enumerate(search_targets):
            is_primary = idx == 0
            for word in self._prefix_candidates(prefix):
                if word == target_bangla:
                    continue
                previous = candidate_flags.get(word, False)
                candidate_flags[word] = previous or is_primary

        candidates = [
            (word, self._score_word(word, is_exact=is_exact))
            for word, is_exact in candidate_flags.items()
        ]

        # Sort by score descending (highest = most relevant)
        candidates.sort(key=lambda x: (-x[1], len(x[0]), x[0]))

        # Deduplicate and return top 5
        result = []
        for word, score in candidates:
            result.append(word)
            if len(result) >= 5:
                break

        return result
