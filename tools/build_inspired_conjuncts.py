#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


BYANJON_RE = re.compile(r'\("([^"]+)"\s+\(set CID\s+(\d+)\)\s+"([^"]+)"\)')
PCID_RE = re.compile(r"\(\(= PCID (\d+)\)")
CID_RE = re.compile(r"\(\(= CID (\d+)\)")
INSERT_RE = re.compile(r'insert "([^"]+)"')


def load_banjon_map(text):
    cid_to_key = {}
    cid_to_bn = {}
    for key, cid, bn in BYANJON_RE.findall(text):
        cid_int = int(cid)
        cid_to_key[cid_int] = key
        cid_to_bn[cid_int] = bn
    return cid_to_key, cid_to_bn


def is_usable_pair(pc_key, cid_key):
    return bool(re.fullmatch(r"[a-z]+", pc_key) and re.fullmatch(r"[a-z]+", cid_key))


def is_usable_insert(inserted):
    if "/" in inserted or " " in inserted:
        return False
    if not re.search(r"[\u0980-\u09FF]", inserted):
        return False
    return True


def extract_pairs(text, cid_to_key):
    pairs = {}
    records = []
    current_pcid = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        pcid_match = PCID_RE.search(line)
        if pcid_match:
            current_pcid = int(pcid_match.group(1))

        if current_pcid is None:
            continue
        if "set SLICER" not in line:
            continue
        if "set ALTERNATE" in line:
            continue

        cid_match = CID_RE.search(line)
        insert_match = INSERT_RE.search(line)
        if not cid_match or not insert_match:
            continue

        cid = int(cid_match.group(1))
        inserted = insert_match.group(1)
        if current_pcid not in cid_to_key or cid not in cid_to_key:
            continue

        pc_key = cid_to_key[current_pcid]
        cid_key = cid_to_key[cid]
        if not is_usable_pair(pc_key, cid_key):
            continue
        if not is_usable_insert(inserted):
            continue

        pair_key = f"{pc_key}{cid_key}"
        if pair_key not in pairs:
            pairs[pair_key] = inserted
            records.append(
                {
                    "pair": pair_key,
                    "insert": inserted,
                    "pcid": current_pcid,
                    "cid": cid,
                }
            )

    return pairs, records


def main():
    parser = argparse.ArgumentParser(description="Build inspired conjunct rules from a local M17n layout.")
    parser.add_argument(
        "--mim",
        default="layout-source.mim",
        help="Path to local .mim layout input",
    )
    parser.add_argument(
        "--out",
        default="data/inspired_conjuncts.json",
        help="Output JSON path",
    )
    args = parser.parse_args()

    mim_path = Path(args.mim)
    if not mim_path.exists():
        candidates = sorted(Path.cwd().glob("*.mim"))
        if candidates:
            mim_path = candidates[0]
        else:
            raise FileNotFoundError(
                f"Layout file not found: {args.mim}. "
                "Provide --mim <path-to-layout.mim>."
            )

    out_path = Path(args.out)
    text = mim_path.read_text(encoding="utf-8")

    cid_to_key, _cid_to_bn = load_banjon_map(text)
    pairs, records = extract_pairs(text, cid_to_key)

    out = {
        "source_type": "external_m17n_layout",
        "source_ref": "local_mim_input",
        "pair_count": len(pairs),
        "pairs": dict(sorted(pairs.items())),
        "records": records,
    }
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(pairs)} pairs to {out_path}")


if __name__ == "__main__":
    main()
