#!/usr/bin/env python3
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_RUNTIME = ROOT / "docs" / "runtime"

PYTHON_FILES = [
    "core/__init__.py",
    "core/engine/__init__.py",
    "core/engine/tokenizer.py",
    "core/engine/normalizer.py",
    "core/engine/dictionary.py",
    "core/engine/phonetic_parser.py",
    "core/engine/suffix_handler.py",
    "core/engine/suggester.py",
    "core/engine/user_dictionary.py",
    "core/engine/context_engine.py",
    "core/engine/loanword_transliterator.py",
    "core/engine/transliterator.py",
]

DATA_FILES = [
    "data/dictionary.json",
    "data/loanwords.json",
    "data/mapping.json",
    "data/patterns.json",
    "data/openbangla_dictionary.json",
    "data/word_frequency.json",
    "data/inspired_conjuncts.json",
    "data/phonetic_overrides.json",
    "data/high_risk_ambiguity.json",
]


def _copy(relative_path):
    src = ROOT / relative_path
    dest = DOCS_RUNTIME / relative_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def build():
    if DOCS_RUNTIME.exists():
        shutil.rmtree(DOCS_RUNTIME)
    DOCS_RUNTIME.mkdir(parents=True, exist_ok=True)

    for rel in PYTHON_FILES + DATA_FILES:
        _copy(rel)

    manifest = {
        "entry_module": "core.engine.transliterator",
        "python_files": PYTHON_FILES,
        "data_files": DATA_FILES,
        "files": PYTHON_FILES + DATA_FILES,
    }
    (DOCS_RUNTIME / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (ROOT / "docs" / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Runtime bundle created at {DOCS_RUNTIME}")


if __name__ == "__main__":
    build()
