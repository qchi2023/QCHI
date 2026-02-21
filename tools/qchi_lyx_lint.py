#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\ref\{([^}]+)\}")
HARDCODED_RE = re.compile(r"\b(?:Equation|Eq\.?|Figure|Fig\.?|Section|Sec\.?)\s+\d+\b")
BAD_LABEL_CMD_RE = re.compile(r"\\label(?!\{)")
BAD_REF_CMD_RE = re.compile(r"\\ref(?!\{)")
LABEL_PREFIX_RE = re.compile(r"^(sec|eq|fig|tab)-")


def lint_file(path: Path, allow_colon: bool):
    text = path.read_text(encoding="utf-8", errors="ignore")
    errors = []

    # Must look like a real LyX file, not markdown/plain text with .lyx extension
    if "\\lyxformat" not in text or "\\begin_document" not in text or "\\end_document" not in text:
        errors.append("file does not look like valid LyX format (missing required LyX document markers)")

    if re.search(r"^#\s", text, flags=re.MULTILINE):
        errors.append("contains markdown headings; likely not a valid LyX document")
    if re.search(r"^-\s", text, flags=re.MULTILINE):
        errors.append("contains markdown bullet syntax; likely not a valid LyX document")

    if not allow_colon and ":" in text:
        errors.append("contains ':' but colon is disallowed by LyX policy")

    if BAD_LABEL_CMD_RE.search(text):
        errors.append("malformed \\label command found (must be \\label{...})")
    if BAD_REF_CMD_RE.search(text):
        errors.append("malformed \\ref command found (must be \\ref{...})")

    labels = set(LABEL_RE.findall(text))
    refs = REF_RE.findall(text)

    bad_prefix = sorted([l for l in labels if not LABEL_PREFIX_RE.match(l)])
    if bad_prefix:
        errors.append(f"labels without required prefix sec/eq/fig/tab: {', '.join(bad_prefix[:8])}")

    missing = sorted({r for r in refs if r not in labels})
    if missing:
        errors.append(f"dangling refs: {', '.join(missing[:8])}")

    if HARDCODED_RE.search(text):
        errors.append("contains hardcoded internal numbering (use \\ref)")

    if not labels and ("\\ref{" in text or "Formula" in text or "begin_layout Section" in text):
        errors.append("has references/structure but no labels found")

    return errors


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--allow-colon", action="store_true")
    args = p.parse_args()

    root = Path(args.root)
    files = sorted(root.rglob("*.lyx"))

    if not files:
        print("PASS lyx lint: no .lyx files found")
        return 0

    failed = 0
    for f in files:
        errs = lint_file(f, allow_colon=args.allow_colon)
        if errs:
            failed += 1
            print(f"FAIL {f}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"PASS {f}")

    if failed:
        print(f"FAIL lyx lint: {failed} file(s) failed")
        return 1

    print("PASS lyx lint")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
