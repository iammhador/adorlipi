# AdorLipi Agent Guide

AdorLipi is a Linux-first Banglish-to-Bangla keyboard built around an IBus input method. The core goal is natural conversational Banglish input, especially the spellings people use in daily social media/chat, converted into accurate Bangla without network calls.

## Repository Map

- `core/engine/` contains the platform-independent Python transliteration engine.
- `data/` contains JSON dictionaries, phonetic mappings, patterns, suggestion data, and word frequency data.
- `platforms/linux/` contains the IBus engine, installer, and package build scripts.
- `cli/main.py` is the interactive debug entrypoint for local transliteration checks.
- `assets/` contains project visual assets.

The main runtime path is:

```text
Input -> pre-process -> tokenize -> normalize -> user dictionary -> exact dictionary
      -> compound/plain suffix root resolution -> skeleton dictionary
      -> loanword (gated) -> fuzzy (gated) -> patterns -> phonetic parser -> output
```

## Development Commands

Run the interactive CLI:

```bash
python3 cli/main.py
```

Run a one-word smoke test:

```bash
python3 -c "from core.engine.transliterator import Transliterator; t=Transliterator(); print(t.transliterate('assignment'))"
```

Run the regression suite:

```bash
python3 -m unittest discover tests/ -v
```

Install the Linux IBus engine from source:

```bash
sudo bash platforms/linux/install.sh
# Then restart IBus as regular user (not root shell)
ibus-daemon -drx
```

## Accuracy Workflow

- Prefer `data/dictionary.json` for ambiguous real-world words, modern vocabulary, English loanwords, names, and conversational spellings.
- Keep external-source-inspired artifacts neutral in tracked names and identifiers (for example: `inspired_*` style names).
- Change `data/mapping.json` or `core/engine/phonetic_parser.py` only when the desired behavior is broad and systematic, because parser/mapping edits can affect many words.
- Add or update regression tests for every fixed Banglish input.
- Treat README examples as public promises. If a README example fails, fix the engine/data or update the README only when the promise is intentionally changing.
- Keep dictionary changes valid JSON and use exact Banglish keys in normalized lowercase unless the key relies on existing case-sensitive mapping behavior.
- For fallback behavior changes, verify `explain_word()` metadata (`source_layer`, `confidence`, `matched_key`) in tests.
- For suggestion ranking changes, add fixture-based tests that do not depend on large production dictionary ordering.

## Docs and Pages Workflow

- The web usage guide lives in `docs/` and is deployed through GitHub Pages.
- Rebuild runtime bundle before docs deployment:

```bash
python3 tools/build_docs_runtime.py
```

- Runtime files for web demo are sourced from `core/` and `data/` and bundled into `docs/runtime/`.

## Runtime Cautions

- The core engine is pure Python and should stay offline/local-only.
- `UserDictionary` stores learned user choices under `~/.config/adorlipi/user_dict.json`; tests should isolate `HOME` or otherwise avoid writing to a real user profile.
- The IBus integration requires Linux with IBus and GI bindings; most engine fixes can be tested through `Transliterator` without launching IBus.
- Installer/package scripts copy files into `/usr/share/adorlipi` and register the IBus component.
- `ibus restart` inside `sudo` installer context may fail because root cannot access the user DBus session; restart IBus from the user session when validating install.
- `platforms/linux/PKGBUILD` currently references `platforms/linux/adorlipi.xml`, while the repo file is `platforms/linux/adorlipi-ibus.xml`; handle that in a packaging-focused change.
