# AdorLipi (আদরলিপি) 🇧🇩

> **The Simple, Open Source Banglish-to-Bangla Transliteration Engine for Linux.**

![License](https://img.shields.io/badge/license-MIT-green) ![Platform](https://img.shields.io/badge/platform-Linux-blue) ![Language](https://img.shields.io/badge/language-Bangla-red)

AdorLipi is a lightweight tool that lets you type in phonetic English ("Banglish") and get proper Bangla output. It works everywhere on your Linux system—browser, terminal, chats, and editors—integrating natively with your keyboard.

**Example:**
- Type: `Ami tomay bhalobashi`
- Get: `আমি তোমায় ভালোবাসি`

---

## 🚀 Installation

We support **all major Linux distributions** including Fedora, Ubuntu, Debian, and Arch.

### One-Step Installer (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/AdorLipi.git
   cd AdorLipi
   ```

    2. **Run the installer:**
       ```bash
       sudo bash install_ibus.sh
       ```

   *This script will automatically detect your distribution (Fedora/Ubuntu), install necessary dependencies, and set up the AdorLipi keyboard for you.*

3. **Restart & Enable:**
   - **Log out and log back in** (or restart your computer) to refresh the keyboard system.
   - Go to **Settings** > **Keyboard** > **Input Sources** (or **Region & Language**).
   - Click `+`.
   - Search for **Bangla** or **Other**.
   - Select **AdorLipi**.
   - Click **Add**.

---

## ⌨️ Usage

### System-Wide Keyboard
Once enabled, simply press `Super + Space` (Windows Key + Space) to switch your keyboard layout to **AdorLipi**.

- Type naturally in key-mapped phonetic styles (e.g., `k` -> `ক`, `kh` -> `খ`).
- Works in **Firefox, Chrome, LibreOffice, Gedit, Discord, VS Code**, and more.

### Command Line Tool
You can also use AdorLipi correctly from your terminal!

```bash
$ adorlipi

initializing AdorLipi...
> valo aso?
ভালো আছো?
```

---

## 🔧 Supported Platforms

AdorLipi is built to be universal. We officially verify:
- **Fedora Workstation** (38+)
- **Ubuntu** (22.04 LTS+)
- **Debian** (12+)
- **Arch Linux** (via manual install)
- **Linux Mint, Pop!_OS, Manjaro**

---

## 🤝 Contributing

We love open source! AdorLipi is community-driven.

### How to help:
1.  **Add Words**: Found a word that doesn't convert right? Open `adorlipi/data/dictionary.json` and add it!
2.  **Fix Logic**: Improve the phonetic engine in `adorlipi/engine/`.
3.  **Report Bugs**: Open an issue on GitHub.

**Pull Requests are welcome!**

## 📚 Phonetic Mapping (Key Layout)

AdorLipi uses intuitive phonetic mapping. Here is the quick reference:

| Key | Bangla | Key | Bangla | Key | Bangla |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **a** | অ | **t** | ত | **p** | প |
| **aa** | আ | **th** | থ | **f** / **ph** | ফ |
| **i** | ই | **d** | দ | **b** | ব |
| **ii** | ঈ | **dh** | ধ | **bh** | ভ |
| **u** | উ | **n** | ন | **m** | ম |
| **uu** | ঊ | **r** | র | **l** | ল |
| **e** | এ | **rr** | ড় | **sh** | শ |
| **oi** | ঐ | **rrh** | ঢ় | **ss** | ষ |
| **o** | ও | **y** | য় | **s** | স |
| **ou** | ঔ | **tt** | ট | **h** | হ |
| **k** | ক | **dd** | ড | **z** | জ |
| **kh** | খ | **c** / **ch** | চ | **ng** | ং |
| **g** | গ | **chh** | ছ | **:** | ঃ |
| **gh** | ঘ | **j** | জ | **^** | ঁ |

### Special Features
- **Dual Suggestion**: 
    - As you type, AdorLipi suggests both the **Bangla** word and the original **English** text.
    - Press `Space` or `Enter` to select the Default (Bangla).
    - Press `2` to select the English word.
    - Use `Up` / `Down` arrows to navigate.

---

## 👨‍💻 For Developers & Contributors

We follow standard open-source practices.

### Project Structure
- `adorlipi/`
    - `engine/`: Core phonetic logic (`transliterator.py`).
    - `data/`: JSON dictionaries and mapping rules.
    - `tools/`: Maintenance scripts (bulk import, generators).

### Setup for Development
1.  **Clone & Install in Editable Mode**:
    ```bash
    git clone https://github.com/iammhador/adorlipi
    cd AdorLipi
    pip3 install -e .
    ```

2.  **Run Development Mode**:
    ```bash
    ./dev.sh
    ```
    *This runs the CLI version for quick testing.*

3.  **Test System Integration**:
    ```bash
    sudo ./install_ibus_dev.sh
    ibus restart
    ```
    *Links your local code to IBus. Any change you make is live after a restart.*

4.  **Run Tests**:
    ```bash
    python3 -m unittest discover tests
    ```

### License
AdorLipi is open-sourced software licensed under the **MIT License**.
Made with ❤️ for the Bangla Open Source Community.
