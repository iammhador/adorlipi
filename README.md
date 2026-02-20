# AdorLipi (আদরলিপি) 🇧🇩

> **The Smartest Banglish-to-Bangla Transliteration Engine for Linux.**

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![Dictionary](https://img.shields.io/badge/dictionary-6000%2B%20words-green) ![Platform](https://img.shields.io/badge/platform-Linux-orange) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

**AdorLipi** is a next-generation phonetic typing tool designed for the modern Bengali user. It allows you to type natural "Banglish" (e.g., *ami tomay bhalobashi*) and instantly converts it to accurate Bangla text (*আমি তোমায় ভালোবাসি*).

Unlike traditional rigid mappers, AdorLipi features a **context-aware dictionary** of over **6,000 words**, covering everything from literary terms to the latest **Gen-Z social media slang** (*chill, para, cringe, lol*).

---

## ✨ Features

- **🚀 6,000+ Word Smart Dictionary**: Handles complex spellings (`pahar` -> `পাহাড়`, `corner` -> `কর্নার`) instantly.
- **📊 Data-Driven Accuracy**: We continuously analyze text from **Social Media** to predict the most natural suggestions and understand how people *actually* type today.
- **📱 Social Media Ready**: Knows internet slang (`lol` -> `লোল`, `bro` -> `ব্রো`, `chill` -> `চিল`).
- **🧠 Phonetic Intelligence**:
  - **Smart 'O' Handling**: Distinguishes when 'o' means 'অ' (*gorom* -> *গরম*) vs 'ও' (*pokka* -> *পোক্কা*).
  - **Automatic Conjuncts**: `kk` -> `ক্ক`, `tr` -> `ত্র`, `ng` -> `ং`.
- **⚡ Zero Latency**: Written in high-performance Python, works instantly on any hardware.
- **🌍 Universal Input**: Works in **any app** (VS Code, Browser, Telegram, Discord, Terminal).

---

## 📁 Project Structure (Monorepo)

```
adorlipi/
├── core/                # Shared transliteration engine
│   └── engine/          # Transliterator, parser, tokenizer, normalizer
├── data/                # Dictionary (6000+ words) & phonetic mappings
├── platforms/
│   └── linux/           # IBus integration (install.sh, ibus_engine.py)
├── cli/                 # Command-line tool for testing
├── corpus/              # Social media training data
├── tools/               # Dictionary maintenance scripts
├── tests/               # All test suites
├── assets/              # Logo & icons
└── docs/                # Documentation
```

> This monorepo architecture allows sharing the `core/` engine across **all future platforms** (Windows, macOS, Android, iOS).

---

## 🛠️ Installation

AdorLipi supports **all major Linux distributions** (Ubuntu, Fedora, Debian, Arch, Manjaro, Kali).

### Quick Install (Recommended)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/iammhador/adorlipi.git
    cd adorlipi
    ```

2.  **Run the installer:**
    ```bash
    sudo bash platforms/linux/install.sh
    ```
    *This script automatically installs IBus and necessary Python dependencies for your specific distro.*

3.  **Activate:**
    - **Restart IBus**:
      ```bash
      ibus restart
      ```
    - Go to **Settings** > **Keyboard** > **Add Input Source** (+).
    - Select **Bangla** (or Other) -> **AdorLipi**.

---

## 🎮 Usage Guide

Once enabled, switch to AdorLipi (usually `Super + Space`) and start typing!

### Basic Typing
| Type | Output |
| :--- | :--- |
| `ami` | আমি |
| `kemon` | কেমন |
| `achen` | আছেন |
| `dhonnobad` | ধন্যবাদ |

### Smart Phrasings
| Type | Output | Context |
| :--- | :--- | :--- |
| `gorom` | গরম | *Not গোরোম* |
| `pagol` | পাগল | *Not পাগোল* |
| `assignment` | অ্যাসাইনমেন্ট | *English mix* |
| `chill` | চিল | *Slang* |

### Key Mapping Reference
| Key | Bangla | Key | Bangla | Key | Bangla |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `k` | ক | `kh` | খ | `g` | গ |
| `t` | ত/ট | `th` | থ/ঠ | `d` | দ/ড |
| `n` | ন | `p` | প | `f` | ফ |
| `b` | ব | `m` | ম | `r` | র |
| `l` | ল | `s` | স | `sh` | শ/ষ |
| `h` | হ | `z`/`j` | জ/য | `y` | য় |

---

## ❓ FAQ

**Q: Does it work on Windows or Mac?**
> The core engine is written in pure Python and is cross-platform. However, the current "driver" is built for **Linux (IBus)**. Windows/Mac ports are planned using the monorepo's `platforms/` structure.

**Q: I found a wrong word! How to fix?**
> AdorLipi is open source! You can edit `data/dictionary.json` and add your word, then run the installer again. Or submit a Pull Request!

---

## 👨‍💻 Contributing

We welcome contributions!
- **Core Engine**: `core/engine/` — transliteration logic.
- **Dictionary**: `data/dictionary.json` — 6000+ word mappings.
- **Platform Drivers**: `platforms/` — OS-specific integration code.
- **Corpus**: `corpus/` — social media data for analysis.

### Run Tests
```bash
python3 -m unittest discover tests/ -v
```

### Run CLI (Debug Mode)
```bash
python3 cli/main.py
```

**License**: MIT  
*Made with ❤️ for the Bangla Open Source Community.*
