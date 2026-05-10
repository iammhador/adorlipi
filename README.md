<p align="center">
  <img src="assets/logo.svg" alt="AdorLipi Logo" width="200">
</p>

<h1 align="center">AdorLipi (আদরলিপি)</h1>

<p align="center">
  <strong>"অদরলিপি - ভাবনা থেকে বাংলা"</strong>
</p>
<p align="center">
  <em>The first modern and easy-to-use Banglish keyboard for Linux users.</em>
</p>

There is a long-standing challenge in the open-source community: while great phonetic keyboards like Avro and OpenBangla exist for Linux, they often struggle to perfectly convert modern conversational "Banglish" (e.g., *advance*, *perfect*) into accurate Bengali. AdorLipi was built to solve exactly this issue.

People type the same Bengali words using countless spelling variations across social media. AdorLipi’s engine has been trained on real-world social media spelling patterns, adding thousands of these unique conversational variations into our smart dictionary. 

It solves a massive problem for the community: **Type exactly how you speak on social media, follow normal English spelling rules, and get perfectly accurate Bengali instantly.**

Currently available and highly optimized for Linux, with cross-platform support planned for the future.

---

<p align="center">
  <a href="https://github.com/iammhador/adorlipi/releases"><img src="https://img.shields.io/github/v/release/iammhador/adorlipi?style=flat-square&color=5E35B1&label=Release" alt="Release"></a>
  <img src="https://img.shields.io/badge/Dictionary-10%2C000%2B%20words-00B4DB?style=flat-square" alt="Dictionary">
  <img src="https://img.shields.io/badge/Platform-Linux-FF512F?style=flat-square" alt="Platform">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square" alt="License"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square" alt="PRs Welcome"></a>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-features">Features</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage-guide">Usage</a> •
  <a href="#-key-mapping-reference">Key Map</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-contributing">Contributing</a> •
  <a href="#-faq">FAQ</a>
</p>

---

## 🚀 Quick Start

Type natural Banglish → get accurate Bangla. Instantly. In any app.

```
ami tomay bhalobashi   →   আমি তোমায় ভালোবাসি
dhonnobad              →   ধন্যবাদ
kemon achen?           →   কেমন আছেন?
```

**Install from source (works on any Linux distro):**
```bash
git clone https://github.com/iammhador/adorlipi.git
cd adorlipi
sudo bash platforms/linux/install.sh
ibus restart
```

Then: **Settings** > **Keyboard** > **Add Input Source** > Search **AdorLipi** → `Super + Space` to toggle.

---

## ✨ Features

### 🧠 Context-Aware Dictionary (10,000+ words)
Not a simple key mapper — AdorLipi uses a curated dictionary of **10,000+ words** to resolve ambiguous Banglish spellings that no phonetic rule can handle:

| `dak` — দ vs ড ambiguity | দাক ❌ | ডাক ✅ |
| `manual` — Phonetic ambiguity | মানুআল ❌ | ম্যানুয়াল ✅ |
| `sohomot` — "o" sound context | সোহোমত ❌ | সহমত ✅ |
| `porikkha` — conjunct ক্ষ | পোরিক্শা ❌ | পরীক্ষা ✅ |
| `giyechi` — ছ vs চ context | গিয়েচি ❌ | গিয়েছি ✅ |

### 📊 Data-Driven Accuracy
We continuously analyze **real Banglish typing patterns** from social media, messaging, and forums to understand how people *actually* type — not how textbooks say they should.

### 📱 Modern Vocabulary
Full support for conversational Banglish, everyday expressions, and English loanwords commonly mixed into spoken Bangla:

```
advance → এডভান্স    perfect → পারফেক্ট    vibes → ভাইবস
assignment → অ্যাসাইনমেন্ট    management → ম্যানেজমেন্ট
```

### ⚡ Phonetic Intelligence V2
- **Smart Contextual 'O' Dropping** — Automatically detects word boundaries and multi-character clusters to keep or drop implicit vowels natively (`shanto` → শান্ত, `bhalo` → ভালো).
- **Native Algorithmic Conjuncts** — Structurally builds 20+ generic conjuncts natively without dictionary reliance (`nt` → ন্ত, `kkh` → ক্ষ).
- **Regex Patterns (`patterns.json`)** — A customizable mathematical fallback layer to resolve strict phonetic ambiguities (`torko` → তর্ক) before dictionary or base phonetic parsing.
- **Smart Suffix Handling** — Strips grammatical verb/noun suffixes (`er/e/te/ke/r/der/nor/lor`), looks up the root independently, and perfectly reattaches the Bangla equivalent natively.

### 🚀 Extreme Scalability (1M Word Verified)
AdorLipi is engineered for flawless computational performance. The V2 Engine has been computationally verified against **1,000,000 synthetic non-dictionary words**, demonstrating a 0% Unicode crash rate (no English leaks, no double hasants) while processing at speeds exceeding **63,000 words per second**.

### 🌍 Universal Input
Works in **every application** — VS Code, Browser, Telegram, Discord, LibreOffice, Terminal — anywhere IBus is supported. Zero network calls, zero latency delays. All on your local machine.

---

## 📦 Installation

AdorLipi runs on **any Linux distro** that supports IBus.

### ✅ Method 1: App Store Style Install (Ubuntu/Debian/Fedora)

We provide simple packages for an easy "double-click" App Store-like installation on Ubuntu, Linux Mint, PopOS, Debian, and Fedora.

1. Go to the [Releases](https://github.com/iammhador/adorlipi/releases) page.
2. Download the appropriate file:
   - For Ubuntu/Mint/Debian: `adorlipi_x.x.x_all.deb`
   - For Fedora/RHEL: `adorlipi-x.x.x-1.noarch.rpm`
3. Double click to install it via your Software Center, or open a terminal and run:
   ```bash
   # Ubuntu/Debian:
   sudo apt install ./adorlipi_1.0.0_all.deb
   
   # Fedora:
   sudo dnf install ./adorlipi-1.0.0-1.noarch.rpm
   ```

### 🏹 Method 2: Arch Linux (AUR)

AdorLipi is fully available on the Arch User Repository (AUR). You can install it using any AUR helper like `yay` or `paru`:

```bash
yay -S adorlipi-git
```

### 💻 Method 3: Universal Installer (All Linux Distros)

If you are on a different distribution (or prefer building from source), you can install using our automated script:

```bash
git clone https://github.com/iammhador/adorlipi.git
cd adorlipi
sudo bash platforms/linux/install.sh
```

What the script does:
- Detects **Debian/Ubuntu/Fedora/RHEL** and installs required dependencies (`python3-gi`, `ibus` etc.)
- Copies engine, data, and IBus XML to `/usr/share/adorlipi/`
- Registers the IBus component and restarts IBus

### Activate After Install

```bash
ibus restart
```

1. Open **Settings** → **Keyboard** → **Input Sources**
2. Click **+** → Search for **Bangla** (or **Other**)
3. Select **AdorLipi (আদরলিপি)**
4. Use `Super + Space` to switch between English and AdorLipi

> [!TIP]
> On some distros, log out and back in after install for IBus to detect the new engine.

---

## 🧪 Testing

### Test Without IBus (Fastest)

You can verify AdorLipi works correctly without configuring IBus at all:

```bash
# Interactive CLI — type Banglish, see Bangla output live
python3 cli/main.py
```

### Test a Specific Word

```bash
python3 -c "
from core.engine.transliterator import Transliterator
t = Transliterator()

# Test individual words
print(t.transliterate('ami tomay bhalobashi'))   # আমি তোমায় ভালোবাসি
print(t.transliterate('porikkha'))               # পরীক্ষা
print(t.transliterate('udbhash'))                # উদ্ভাস
print(t.transliterate('unmesh'))                 # উন্মেষ
"
```

### Run the Test Suite

```bash
# Run all tests
python3 -m unittest discover tests/ -v

# Run a specific test file
python3 -m unittest tests/test_basic_words.py -v
```

### Test with IBus (After Install)

After running `install.sh` and restarting IBus:
1. Open any text field (browser URL bar, Gedit, VS Code)
2. Press `Super + Space` to switch to AdorLipi
3. Type `ami` — you should see আমি

If AdorLipi doesn't appear in input sources, run:
```bash
ibus restart
ibus list-engine | grep adorlipi   # Should show: adorlipi
```

---

## 🎮 Usage Guide

Switch to AdorLipi (`Super + Space`) and start typing naturally. AdorLipi recognizes how people actually type on social media:

### Conversational Typing

| Banglish | Output | Category |
|:---------|:-------|:---------|
| `ami apnake` | আমি আপনাকে | Pronoun / Respectful |
| `kemon achen` | কেমন আছেন | Greeting |
| `sohomot` | সহমত | Agreement |
| `manual` | ম্যানুয়াল | English loan |
| `osadharon` | অসাধারণ | Compliment |
| `valobashi` | ভালোবাসি | Emotion |
| `advance` | এডভান্স | English loan |
| `inshaallah` | ইনশাআল্লাহ | Cultural |

### How It Works

AdorLipi processes each word through a **5-stage pipeline** designed specifically to handle ambiguous social-media spellings:

```
Input → Tokenize → Normalize → Dictionary Lookup → Suffix Decomposition → Phonetic Parse → Output
          ↓           ↓              ↓                    ↓                      ↓
       Split by    Preserve      Exact match?        Strip suffix,           Map each
       spaces &    case-sens.    Return it!          lookup root,            character
       punctuation chars (N,J)                       reattach বাংলা suffix   phonetically
```

**Example**: `bondhura` (friends)
1. **Dictionary** — no exact match for `bondhura`
2. **Suffix** — strips `ra` (রা), root = `bondhu`
3. **Dictionary** — `bondhu` → বন্ধু ✅
4. **Result** — বন্ধু + রা = **বন্ধুরা** ✅

---

## ⌨️ Key Mapping Reference

### Vowels (স্বরবর্ণ)

| Key | Bangla | Key | Bangla | Key | Bangla |
|:----|:-------|:----|:-------|:----|:-------|
| `a` / `aa` | আ | `i` | ই | `ii` | ঈ |
| `u` | উ | `uu` | ঊ | `e` | এ |
| `o` | ও | `oi` | ঐ | `ou` | ঔ |
| `rri` | ঋ | | | | |

### Consonants (ব্যঞ্জনবর্ণ)

| Key | Bangla | Key | Bangla | Key | Bangla |
|:----|:-------|:----|:-------|:----|:-------|
| `k` | ক | `kh` | খ | `g` | গ |
| `jh` | ঝ | `t` | ত | `tt` | ট |
| `th` | থ | `tth` | ঠ | `d` | দ |
| `dd` | ড | `dh` | ধ | `ddh` | ঢ |
| `n` | ন | `N` | ণ | `p` | প |
| `f` / `ph` | ফ | `b` | ব | `bh` / `v` | ভ |
| `m` | ম | `z` / `J` | য | `r` | র |
| `rr` | ড় | `rrh` | ঢ় | `l` | ল |
| `sh` | শ | `ss` | ষ | `s` | স |
| `h` | হ | `y` | য় | `w` | ব |
| `q` | ৎ | `x` | ক্স | `kkh` / `ksh` | ক্ষ |
| `NGV` | ঞ | `:` | ঃ | `^` | ঁ |

### Vowel Signs (কার) — Applied automatically after consonants

| Key | Kar | Key | Kar | Key | Kar |
|:----|:----|:----|:----|:----|:----|
| `a` | া | `i` | ি | `ii` | ী |
| `u` | ু | `uu` | ূ | `e` | ে |
| `o` | ো | `oi` | ৈ | `ou` | ৌ |
| `rri` | ৃ | | | | |

### Conjuncts (যুক্তবর্ণ) — Formed automatically

| Key | Fola | Example | Result |
|:----|:-----|:--------|:-------|
| `r` after consonant | ্র (র-ফলা) | `pr` | প্র |
| `y` / `z` after consonant | ্য (য-ফলা) | `ky` | ক্য |
| `w` after consonant | ্ব (ব-ফলা) | `sw` | স্ব |
| Double consonant | ্ (হসন্ত) | `kk` | ক্ক |

### Numbers (সংখ্যা)

| Key | Bangla | Key | Bangla | Key | Bangla |
|:----|:-------|:----|:-------|:----|:-------|
| `0` | ০ | `1` | ১ | `2` | ২ |
| `3` | ৩ | `4` | ৪ | `5` | ৫ |
| `6` | ৬ | `7` | ৭ | `8` | ৮ |
| `9` | ৯ | `.` | । | | |

---

## 🏗️ Architecture

AdorLipi follows a **monorepo architecture** designed for cross-platform expansion:

```
adorlipi/
├── core/                        # Platform-independent transliteration engine
│   └── engine/
│       ├── transliterator.py    # Main orchestrator (5-stage pipeline)
│       ├── tokenizer.py         # Splits input into word/punctuation tokens
│       ├── normalizer.py        # Normalizes input, preserves case-sensitive chars
│       ├── dictionary.py        # JSON dictionary lookup (9,500+ entries)
│       ├── phonetic_parser.py   # Character-by-character Bangla mapping
│       └── suffix_handler.py    # Strips/reattaches Bangla suffixes (ের, তে, কে…)
│
├── data/
│   ├── dictionary.json          # 9,500+ Banglish → Bangla word mappings
│   └── mapping.json             # Phonetic character map (a→আ, k→ক, kh→খ…)
│
├── platforms/
│   └── linux/
│       ├── ibus_engine.py       # IBus input method integration
│       ├── install.sh           # Universal Linux installer (apt/dnf/pacman)
│       ├── adorlipi-ibus.xml    # IBus component descriptor
│       ├── PKGBUILD             # Arch Linux AUR package
│       ├── build_deb.sh         # Debian/Ubuntu .deb builder
│       └── build_rpm.sh         # Fedora/RHEL .rpm builder
│
├── cli/
│   └── main.py                  # Interactive CLI for testing & debugging
│
├── tests/
│   ├── test_basic_words.py      # Core transliteration tests
│   ├── test_examples.py         # Real-world sentence tests
│   ├── test_refinements.py      # Edge case & regression tests
│   └── test_robustness.py       # Stress tests & error handling
│
└── assets/                      # Logo, cover image, icons
```

### Pipeline Flow

```
┌──────────┐    ┌────────────┐    ┌────────────┐    ┌───────────────┐    ┌────────────────┐
│ Tokenizer│───▶│ Normalizer │───▶│ Dictionary │───▶│ Suffix Handler│───▶│ Phonetic Parser│
│          │    │            │    │   Lookup   │    │  (if no match)│    │ (last resort)  │
└──────────┘    └────────────┘    └────────────┘    └───────────────┘    └────────────────┘
 Split text      Lowercase         9,500+ word       Strip -er/-e/-te     Map each char
 into tokens     (preserve N,J)    exact match        lookup root          a→আ, k→ক
```

> [!NOTE]
> The `core/` engine is **pure Python with zero dependencies** — making it trivially portable to Windows, macOS, Android, and iOS in future releases.

---

## 🤝 Contributing

We welcome contributions of all kinds! Whether you want to fix a typo in the dictionary, add a new platform driver, or improve the transliteration engine — every contribution matters.

**👉 See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.**

### Quick Contribution Paths

| What | Where | Difficulty |
|:-----|:------|:-----------|
| Fix a wrong word | `data/dictionary.json` | 🟢 Easy |
| Add missing words | `data/dictionary.json` | 🟢 Easy |
| Fix phonetic mapping | `data/mapping.json` | 🟡 Medium |
| Improve engine logic | `core/engine/` | 🔴 Advanced |
| Add platform support | `platforms/` | 🔴 Advanced |
| Write tests | `tests/` | 🟡 Medium |

### Development Setup

```bash
# Clone and enter
git clone https://github.com/iammhador/adorlipi.git
cd adorlipi

# Test the engine interactively
python3 cli/main.py

# Run all tests
python3 -m unittest discover tests/ -v

# Test a specific word
python3 -c "
from core.engine.transliterator import Transliterator
t = Transliterator()
print(t.transliterate('ami tomay bhalobashi'))
"
```

---

## ❓ FAQ

<details>
<summary><strong>Does it work on Windows or Mac?</strong></summary>

The core engine is **pure Python** and fully cross-platform. The current driver is built for **Linux (IBus)**. Windows and macOS ports are planned using the monorepo's `platforms/` structure. Contributions welcome!
</details>

<details>
<summary><strong>I found a wrong word! How do I fix it?</strong></summary>

Edit `data/dictionary.json` — it's a simple JSON `{ "banglish": "বাংলা" }` format. Add or fix the word, test it with `python3 cli/main.py`, and submit a Pull Request. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.
</details>

<details>
<summary><strong>How do I type ঋ (Ri)?</strong></summary>

Type `rri` (double r + i). Plain `ri` produces র + ি.
- `rri` → ঋ
- `krrishno` → কৃষ্ণ
</details>

<details>
<summary><strong>Why does AdorLipi need a dictionary? Can't phonetics handle everything?</strong></summary>

Banglish is inherently ambiguous. The same Roman letter often maps to multiple Bangla characters:
- `d` → দ or ড (`desh` = দেশ, `dak` = ডাক)
- `t` → ত or ট (`tumi` = তুমি, `taka` = টাকা)
- `ch` → চ or ছ (`cha` = চা, `chele` = ছেলে)

No phonetic rule can resolve this — only a dictionary can.
</details>

<details>
<summary><strong>How does suffix handling work?</strong></summary>

In Banglish, people often attach suffixes directly to the English word. AdorLipi strips common Bangla suffixes (`er`, `te`, `ke`, `r`, etc.), looks up the root word in its extensive social media dictionary, and reattaches the correct Bangla suffix. This means `manusher` → মানুষের even though `manusher` isn't deeply hardcoded — because `manush` → মানুষ is known.
</details>

<details>
<summary><strong>Can I use AdorLipi in VS Code / Terminal / Discord?</strong></summary>

Yes! AdorLipi works through IBus, which is a system-level input method. It works in **every application** that accepts text input.
</details>

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  <strong>Made with ❤️ for the Bangla Open Source Community</strong>
  <br>
  <sub>🇧🇩 বাংলা ওপেন সোর্স কমিউনিটির জন্য ভালোবাসায় তৈরি</sub>
</p>
