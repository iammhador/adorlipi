class Tokenizer {
    tokenize(text) {
        return text.match(/\w+|[^\w\s]+|\s+/g) || [];
    }
    is_word(token) {
        return /^\w+$/.test(token);
    }
}

class Normalizer {
    constructor() {
        this.case_sensitive_chars = new Set(['N', 'J']);
        this.case_sensitive_combos = new Set(['NG', 'NGV']);
        this.replacements = [
            [/ph/g, 'f'],
            [/tmi/g, 'tumi']
        ];
    }
    normalize(word) {
        let preserved = word;
        preserved = preserved.replace(/NGV/g, '\\x01NGV\\x01');
        preserved = preserved.replace(/NG/g, '\\x01NG\\x01');

        let result = [];
        let i = 0;
        while (i < preserved.length) {
            if (preserved[i] === '\\x01') {
                let end = preserved.indexOf('\\x01', i + 1);
                result.push(preserved.substring(i + 1, end));
                i = end + 1;
            } else if (this.case_sensitive_chars.has(preserved[i])) {
                result.push(preserved[i]);
                i++;
            } else {
                result.push(preserved[i].toLowerCase());
                i++;
            }
        }
        word = result.join('');
        word = word.replace(/(.)\\1{2,}/g, '$1');

        for (let [pattern, replacement] of this.replacements) {
            word = word.replace(pattern, replacement);
        }
        return word;
    }
}

class SuffixHandler {
    constructor() {
        this.suffixes = [
            ["gulo", "গুলো"],
            ["gula", "গুলা"],
            ["der", "দের"],
            ["ra", "রা"],
            ["ta", "টা"],
            ["ti", "টি"],
            ["te", "তে"],
            ["ke", "কে"],
            ["er", "ের"]
        ];
    }
    strip_suffix(word) {
        for (let [suffix_en, suffix_bn] of this.suffixes) {
            if (word.endsWith(suffix_en)) {
                if (word.length > suffix_en.length + 1) {
                    let root = word.slice(0, -suffix_en.length);
                    return [root, suffix_bn];
                }
            }
        }
        return [word, null];
    }
}

class Dictionary {
    constructor(data) {
        this.dictionary = data || {};
        this.skeleton_index = {};
        this._build_skeletons();
    }

    _to_skeleton(word) {
        if (!word) return word;
        let sk = word[0];
        for (let i = 1; i < word.length; i++) {
            let c = word[i];
            if (!['a', 'e', 'i', 'o', 'u', 'O'].includes(c)) {
                sk += c;
            }
        }
        return sk;
    }

    _build_skeletons() {
        for (let key in this.dictionary) {
            if (key.length <= 3) continue;
            let sk = this._to_skeleton(key);
            if (!this.skeleton_index[sk] || key.length < this.skeleton_index[sk].length) {
                this.skeleton_index[sk] = key;
            }
        }
    }

    // Levenshtein distance for fuzzy matching
    _levenshtein(a, b) {
        if (a.length === 0) return b.length;
        if (b.length === 0) return a.length;
        let matrix = [];
        for (let i = 0; i <= b.length; i++) matrix[i] = [i];
        for (let j = 0; j <= a.length; j++) matrix[0][j] = j;
        for (let i = 1; i <= b.length; i++) {
            for (let j = 1; j <= a.length; j++) {
                if (b.charAt(i - 1) == a.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1,
                        Math.min(matrix[i][j - 1] + 1, matrix[i - 1][j] + 1)
                    );
                }
            }
        }
        return matrix[b.length][a.length];
    }

    exact_lookup(word) {
        return this.dictionary[word.toLowerCase()] || null;
    }

    lookup(word) {
        word = word.toLowerCase();

        // 1. Exact Match
        if (this.dictionary[word]) return this.dictionary[word];

        // 2. Skeleton Match
        if (word.length >= 3) {
            let sk = this._to_skeleton(word);
            if (sk === word && this.skeleton_index[sk]) {
                return this.dictionary[this.skeleton_index[sk]];
            }
        }

        // 3. Fuzzy Match
        if (word.length >= 4) {
            let bestMatch = null;
            let bestScore = 0;
            // Scan keys (can be slow for 25k in JS, we optimize by length difference to skip quickly)
            for (let key in this.dictionary) {
                if (Math.abs(key.length - word.length) > 2) continue;
                let dist = this._levenshtein(word, key);
                let score = 1 - (dist / Math.max(word.length, key.length));
                if (score > bestScore) {
                    bestScore = score;
                    bestMatch = key;
                }
            }
            if (bestScore >= 0.80 && bestMatch) {
                return this.dictionary[bestMatch];
            }
        }

        return null;
    }
}

class PhoneticParser {
    constructor(mapping) {
        this.vowels = mapping.vowels || {};
        this.consonants = mapping.consonants || {};
        this.kars = mapping.kars || {};
        this.folas = mapping.folas || {};

        const all_keys = [
            ...Object.keys(this.vowels),
            ...Object.keys(this.consonants),
            ...Object.keys(this.kars),
            ...Object.keys(this.folas)
        ];
        this.max_key_len = all_keys.length > 0 ? Math.max(...all_keys.map(k => k.length)) : 1;
    }

    parse(word) {
        let i = 0;
        let n = word.length;
        let output = [];
        let last_was_consonant = false;
        let implicit_vowel_dropped = false;
        let last_parsed_chunk = null;

        while (i < n) {
            let match_found = false;
            for (let length = this.max_key_len; length > 0; length--) {
                if (i + length > n) continue;

                let chunk = word.slice(i, i + length);
                let lower_chunk = chunk;

                // Fola Triggers
                if (last_was_consonant && this.folas.hasOwnProperty(lower_chunk)) {
                    let fola_val = this.folas[lower_chunk];
                    if (output.length > 0 && output[output.length - 1].endsWith("\\u09cd") && fola_val.startsWith("\\u09cd")) {
                        output.push(fola_val.substring(1));
                    } else {
                        output.push(fola_val);
                    }
                    i += length;
                    last_was_consonant = true;
                    implicit_vowel_dropped = false;
                    last_parsed_chunk = lower_chunk;
                    match_found = true;
                    break;
                }

                // Double Consonant
                if (last_was_consonant && this.consonants.hasOwnProperty(lower_chunk)) {
                    if (last_parsed_chunk === lower_chunk && lower_chunk.length === 1) {
                        output.push("\\u09cd");
                        output.push(this.consonants[lower_chunk]);
                        i += length;
                        last_was_consonant = true;
                        implicit_vowel_dropped = false;
                        last_parsed_chunk = lower_chunk;
                        match_found = true;
                        break;
                    }
                }

                // Contextual Ref
                if (!last_was_consonant && lower_chunk === 'r' && i + 1 < n) {
                    let next_char = word[i + 1];
                    if (this.consonants.hasOwnProperty(next_char)) {
                        if (!implicit_vowel_dropped) {
                            output.push("\\u09b0\\u09cd");
                            i += length;
                            last_was_consonant = true;
                            implicit_vowel_dropped = false;
                            last_parsed_chunk = lower_chunk;
                            match_found = true;
                            break;
                        }
                    }
                }

                // Consonants
                if (this.consonants.hasOwnProperty(lower_chunk)) {
                    output.push(this.consonants[lower_chunk]);
                    i += length;
                    last_was_consonant = true;
                    implicit_vowel_dropped = false;
                    last_parsed_chunk = lower_chunk;
                    match_found = true;
                    break;
                }

                // Vowels
                if (this.vowels.hasOwnProperty(lower_chunk)) {
                    let is_o = (lower_chunk === 'o' || lower_chunk === 'O');

                    if (last_was_consonant) {
                        if (is_o) {
                            let drop_o = false;
                            if (i + length === n) {
                                drop_o = false;
                                if (last_parsed_chunk && this.consonants.hasOwnProperty(last_parsed_chunk)) {
                                    let bn_char = this.consonants[last_parsed_chunk];
                                    if (bn_char.length > 1) {
                                        drop_o = true;
                                    }
                                }
                            } else {
                                let next_chunk = word.substring(i + length);
                                let temp_i = 0;
                                let cons_count = 0;
                                while (temp_i < next_chunk.length) {
                                    let matched = false;
                                    for (let c_len = this.max_key_len; c_len > 0; c_len--) {
                                        if (temp_i + c_len <= next_chunk.length) {
                                            let chunk_key = next_chunk.slice(temp_i, temp_i + c_len);
                                            if (this.consonants.hasOwnProperty(chunk_key)) {
                                                let bn_val = this.consonants[chunk_key];
                                                cons_count += (bn_val.length > 1) ? 2 : 1;
                                                temp_i += c_len;
                                                matched = true;
                                                break;
                                            }
                                        }
                                    }
                                    if (!matched) break;
                                }

                                if (cons_count === 0) {
                                    drop_o = false;
                                } else if (cons_count >= 2) {
                                    drop_o = true;
                                } else if (cons_count === 1 && temp_i === next_chunk.length) {
                                    if ((last_parsed_chunk === 'n' || last_parsed_chunk === 'l') && next_chunk === 'r') {
                                        drop_o = false;
                                    } else {
                                        drop_o = true;
                                    }
                                } else {
                                    drop_o = false;
                                }
                            }

                            if (drop_o) {
                                implicit_vowel_dropped = true;
                                last_was_consonant = false;
                                last_parsed_chunk = null;
                            } else {
                                let kar = this.kars[lower_chunk];
                                if (kar !== undefined) {
                                    output.push(kar);
                                } else {
                                    output.push(this.vowels[lower_chunk]);
                                }
                                last_was_consonant = false;
                                implicit_vowel_dropped = false;
                                last_parsed_chunk = null;
                            }
                        } else {
                            let kar = this.kars[lower_chunk];
                            if (kar !== undefined) {
                                output.push(kar);
                            } else {
                                output.push(this.vowels[lower_chunk]);
                            }
                            last_was_consonant = false;
                            implicit_vowel_dropped = false;
                            last_parsed_chunk = null;
                        }
                    } else {
                        output.push(this.vowels[lower_chunk]);
                        last_was_consonant = false;
                        implicit_vowel_dropped = false;
                        last_parsed_chunk = null;
                    }
                    i += length;
                    match_found = true;
                    break;
                }
            }

            if (match_found) continue;

            output.push(word[i]);
            i++;
            last_was_consonant = false;
            implicit_vowel_dropped = false;
            last_parsed_chunk = null;
        }

        return output.join("");
    }
}

class Transliterator {
    constructor(dictionaryData, mappingData, patternsData) {
        this.tokenizer = new Tokenizer();
        this.normalizer = new Normalizer();
        this.dictionary = new Dictionary(dictionaryData);
        this.phonetic_parser = new PhoneticParser(mappingData);
        this.suffix_handler = new SuffixHandler();
        this.patterns = patternsData?.patterns || [];
    }

    _pre_process(text) {
        const suffixes = ['e', 'er', 'te', 'k', 'ke', 're', 'der'];
        for (let suf of suffixes) {
            // \\b does not work reliably with Banglish and unicode, using (?<=[a-zA-Z]) instead
            const regex = new RegExp(`(?<=[a-zA-Z])\\\\s+(${suf})(?=[\\\\s\\\\.,!\\\\?]|$|\\\\n)`, 'g');
            text = text.replace(regex, '$1');
        }
        return text;
    }

    transliterate(text) {
        text = this._pre_process(text);
        const tokens = this.tokenizer.tokenize(text);
        let result = [];

        for (let token of tokens) {
            if (this.tokenizer.is_word(token)) {
                let norm_word = this.normalizer.normalize(token);
                let dict_match = this.dictionary.lookup(norm_word);

                if (dict_match) {
                    result.push(dict_match);
                } else {
                    let [root, suffix_bn] = this.suffix_handler.strip_suffix(norm_word);
                    if (suffix_bn) {
                        let root_match = this.dictionary.lookup(root);
                        if (root_match) {
                            result.push(root_match + suffix_bn);
                            continue;
                        }
                    }

                    let pattern_matched = false;
                    for (let pat of this.patterns) {
                        let regex = new RegExp(pat.regex);
                        if (regex.test(norm_word)) {
                            let parsed = norm_word.replace(regex, pat.replace);
                            result.push(parsed);
                            pattern_matched = true;
                            break;
                        }
                    }
                    if (pattern_matched) continue;

                    result.push(this.phonetic_parser.parse(norm_word));
                }
            } else {
                result.push(this.phonetic_parser.parse(token));
            }
        }
        return result.join("");
    }
}

// Export for module systems or attach to window
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Transliterator };
} else {
    window.Transliterator = Transliterator;
}
