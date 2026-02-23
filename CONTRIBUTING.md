# Contributing to AdorLipi (আদরলিপি)

First off, thank you for considering contributing to AdorLipi! 🎉 Every contribution helps build the first modern, easy-to-use Banglish keyboard for Linux users.

This document provides guidelines and instructions for contributing to this project.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#-reporting-bugs)
  - [Suggesting New Words](#-suggesting-new-words)
  - [Improving Phonetic Mapping](#-improving-phonetic-mapping)
  - [Writing Code](#-writing-code)
  - [Adding Platform Support](#-adding-platform-support)
  - [Writing Tests](#-writing-tests)
- [Development Setup](#development-setup)
- [Project Architecture](#project-architecture)
- [Pull Request Process](#pull-request-process)
- [Commit Convention](#commit-convention)
- [Dictionary Contribution Guide](#dictionary-contribution-guide)
- [Style Guide](#style-guide)

---

## Code of Conduct

This project follows a simple code of conduct: **be respectful, be constructive, be inclusive**. We want AdorLipi to be a welcoming project for contributors of all backgrounds and skill levels. Harassment, discrimination, or toxic behavior will not be tolerated.

---

## How Can I Contribute?

### 🐛 Reporting Bugs

Found a word that transliterates incorrectly? Or is the engine crashing? 

**Open a [GitHub Issue](https://github.com/iammhador/adorlipi/issues/new)** with:

1. **What you typed** (the Banglish input)
2. **What you got** (the incorrect Bangla output)
3. **What you expected** (the correct Bangla output)
4. **Your environment** (distro, IBus version)

**Example:**
```
Input:    porikkha
Got:      পোরিক্শা
Expected: পরীক্ষা
Distro:   Ubuntu 24.04, IBus 1.5.29
```

---

### 📝 Suggesting New Words

This is the **easiest and most impactful** way to contribute. The dictionary (`data/dictionary.json`) is a simple JSON file:

```json
{
  "banglish_word": "বাংলা_ওয়ার্ড"
}
```

**To add words:**

1. Open `data/dictionary.json`
2. Add your word(s) in alphabetical order
3. Test with the CLI: `python3 cli/main.py`
4. Submit a Pull Request

**What words to add:**
- ✅ Words that the phonetic engine gets wrong
- ✅ Common Banglish spellings that people actually type on social media
- ✅ Regional dialects and variations
- ✅ Conversational Banglish, tech terms, English loanwords
- ✅ Islamic/religious terms commonly written in Banglish
- ✅ Proper nouns (places, common names)

**What to avoid:**
- ❌ Extremely rare or archaic words nobody types in Banglish
- ❌ Words that the phonetic engine already handles correctly
- ❌ Offensive or inappropriate content

> [!TIP]
> Test before submitting! Run `python3 -c "from core.engine.transliterator import Transliterator; t = Transliterator(); print(t.transliterate('your_word'))"` to see if the word is already handled.

---

### 🔧 Improving Phonetic Mapping

The phonetic mapping (`data/mapping.json`) defines how Roman characters convert to Bangla:

```json
{
  "k": "ক",
  "kh": "খ",
  "g": "গ"
}
```

If you believe a mapping is incorrect or a new mapping is needed:

1. **Check the existing mapping** — the longer match always takes precedence (`kh` matches before `k`)
2. **Consider side effects** — changing a mapping affects ALL words
3. **Add tests** for the new behavior
4. **Open a discussion issue first** before making mapping changes

> [!CAUTION]
> Mapping changes are high-impact. A single change can affect thousands of words. Always discuss in an issue first and provide comprehensive test cases.

---

### 💻 Writing Code

Contributions to the core engine, normalizer, suffix handler, or platform drivers are welcome.

**Areas that need help:**
- Improving suffix decomposition accuracy
- Adding new platform drivers (Windows, macOS)
- Performance optimization
- Better handling of ambiguous phonetic patterns
- UI/UX for keyboard switching indicators

---

### 🖥️ Adding Platform Support

AdorLipi's monorepo architecture is designed for cross-platform expansion. To add a new platform:

1. Create a new directory: `platforms/<os_name>/`
2. Implement the input method integration for that OS
3. Import and use `core.engine.transliterator.Transliterator`
4. Add an installer script
5. Document installation steps

**Planned platforms:**
- [ ] Windows (via TSF or IME)
- [ ] macOS (via Input Method Kit)
- [ ] Android (via custom keyboard)
- [ ] iOS (via custom keyboard)

---

### ✅ Writing Tests

Tests are in the `tests/` directory and use Python's `unittest` framework.

```bash
# Run all tests
python3 -m unittest discover tests/ -v

# Run a specific test file
python3 -m unittest tests/test_basic_words.py -v
```

**When to add tests:**
- Every dictionary change should have a corresponding test
- Every engine change must not break existing tests
- Edge cases and regression tests are always welcome

**Test file structure:**
```python
import unittest
from core.engine.transliterator import Transliterator

class TestYourFeature(unittest.TestCase):
    def setUp(self):
        self.t = Transliterator()
    
    def test_your_word(self):
        self.assertEqual(self.t.transliterate('banglish'), 'বাংলা')

if __name__ == '__main__':
    unittest.main()
```

---

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- IBus (for testing the Linux driver)

### Setup Steps

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/<your-username>/adorlipi.git
cd adorlipi

# 3. Create a feature branch
git checkout -b feature/your-feature-name

# 4. Make your changes

# 5. Test interactively
python3 cli/main.py

# 6. Run the test suite
python3 -m unittest discover tests/ -v

# 7. Test a specific transliteration
python3 -c "
from core.engine.transliterator import Transliterator
t = Transliterator()
print(t.transliterate('your test input'))
"

# 8. Commit and push
git add -A
git commit -m "feat: add new words for food category"
git push origin feature/your-feature-name

# 9. Open a Pull Request on GitHub
```

### Local Testing (IBus)

To test your changes with the actual IBus keyboard:

```bash
# Install your modified version
sudo bash platforms/linux/install.sh

# Restart IBus
ibus restart

# Now switch to AdorLipi in any app and test
```

---

## Project Architecture

```
adorlipi/
├── core/engine/                 # The brain — platform-independent
│   ├── transliterator.py        # Main entry point, orchestrates the pipeline
│   ├── tokenizer.py             # Splits "ami tomay" → ["ami", " ", "tomay"]
│   ├── normalizer.py            # "Korbo" → "korbo" (preserves N, J, NG)
│   ├── dictionary.py            # Looks up "porikkha" → "পরীক্ষা"
│   ├── phonetic_parser.py       # Maps "k"→"ক", handles vowels/conjuncts
│   └── suffix_handler.py        # "manusher" → root:"manush" + suffix:"ের"
│
├── data/                        # All data files (no code logic)
│   ├── dictionary.json          # 9,500+ word mappings
│   └── mapping.json             # Character-level phonetic map
│
├── platforms/linux/             # Linux IBus driver
├── cli/                         # Debug CLI tool
└── tests/                       # Test suites
```

### Transliteration Pipeline

Each word goes through these stages **in order**:

| Stage | Component | Purpose | Example |
|:------|:----------|:--------|:--------|
| 1 | **Tokenizer** | Split input into words + punctuation | `"ami. tumi"` → `["ami", ".", " ", "tumi"]` |
| 2 | **Normalizer** | Lowercase input, preserve `N`/`J`/`NG` | `"Korbo"` → `"korbo"` |
| 3 | **Dictionary** | Exact match lookup (9,500+ words) | `"porikkha"` → `"পরীক্ষা"` ✅ done |
| 4 | **Suffix Handler** | Strip suffix, lookup root, reattach | `"manusher"` → `"manush"` + `"ের"` |
| 5 | **Phonetic Parser** | Character-by-character mapping | `"bh"` → `"ভ"`, `"a"` → `"া"` |

> The pipeline is **short-circuiting** — if stage 3 finds a match, stages 4-5 are skipped.

---

## Pull Request Process

1. **Fork** the repository and create a feature branch
2. **Make** your changes with clear, atomic commits
3. **Test** — all existing tests must pass, add new tests for new behavior
4. **Document** — update README if you add new features
5. **Submit** a Pull Request with a clear description

### PR Description Template

```markdown
## What does this PR do?
Brief description of the change.

## Type of Change
- [ ] Dictionary addition (new words)
- [ ] Bug fix (incorrect transliteration)
- [ ] New feature
- [ ] Mapping change
- [ ] Documentation update

## Testing
- [ ] All existing tests pass
- [ ] Added new tests for this change
- [ ] Tested with CLI (`python3 cli/main.py`)

## Examples
| Input | Before | After |
|:------|:-------|:------|
| `word` | wrong_output | correct_output |
```

### Review Criteria

- **Dictionary PRs** — merged quickly if words are correct
- **Mapping PRs** — require discussion and comprehensive testing
- **Engine PRs** — require tests, documentation, and review
- **Platform PRs** — require testing on the target platform

---

## Commit Convention

We follow a simplified [Conventional Commits](https://www.conventionalcommits.org/) format:

| Prefix | Use Case | Example |
|:-------|:---------|:--------|
| `feat:` | New feature or words | `feat: add 500 food-related words` |
| `fix:` | Bug fix | `fix: ch→ছ mapping for giyechi` |
| `docs:` | Documentation | `docs: update README installation` |
| `test:` | Tests | `test: add suffix handler tests` |
| `refactor:` | Code refactor | `refactor: simplify normalizer logic` |
| `chore:` | Maintenance | `chore: clean up batch scripts` |

---

## Dictionary Contribution Guide

### File Format

`data/dictionary.json` is a flat JSON object:

```json
{
  "ami": "আমি",
  "tumi": "তুমি",
  "bhalobashi": "ভালোবাসি"
}
```

### Guidelines

1. **Key** = the Banglish spelling people actually type (lowercase)
2. **Value** = the correct Bangla output
3. **No duplicates** — check if the word already exists
4. **Test first** — run `python3 cli/main.py` and type the word. If it already works correctly via phonetic mapping, you don't need to add it
5. **Suffixed forms** — add both root and common suffixed forms:
   ```json
   "porikkha": "পরীক্ষা",
   "porikshar": "পরীক্ষার"
   ```

### Common Suffix Patterns

| Banglish Suffix | Bangla | Meaning | Example |
|:----------------|:-------|:--------|:--------|
| `-r` or `-er` | ের | Possessive | `desher` → দেশের |
| `-e` | এ / -ে | Locative | `deshe` → দেশে |
| `-te` | তে | Locative | `barite` → বাড়িতে |
| `-ke` | কে | Accusative | `tomake` → তোমাকে |
| `-ra` or `-era` | রা / এরা | Plural | `chelera` → ছেলেরা |
| `-der` | দের | Plural poss. | `bondhudeer` → বন্ধুদের |
| `-gulo` | গুলো | Plural | `boigulo` → বইগুলো |
| `-ta` | টা | Definite | `boita` → বইটা |

---

## Style Guide

### Python

- **Python 3.8+** compatible
- Use **docstrings** for all public methods
- Keep functions **small and focused**
- No external dependencies in `core/` — it must remain pure Python
- Follow PEP 8 style guidelines

### JSON

- Use **2-space indentation** for `dictionary.json` and `mapping.json`
- Keep entries **sorted alphabetically** when practical
- Use **UTF-8 encoding** with `ensure_ascii=False`

---

## Questions?

If you have any questions about contributing, feel free to:
- Open a [GitHub Discussion](https://github.com/iammhador/adorlipi/discussions)
- Open an [Issue](https://github.com/iammhador/adorlipi/issues)

---

<p align="center">
  <strong>Thank you for helping make Bangla typing better! 🙏</strong>
</p>
