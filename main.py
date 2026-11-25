"""One Line, One Laugh: Roast Your Fridge.

Writes a single-line fridge roast to /output/entry.txt.
Gate: UTF-8 text, 1-200 characters, not only whitespace, one line.
Pure Python standard library only.
"""

import os
import sys

ENTRY = (
    "My fridge hums all night like it pays rent, yet the only thing "
    "it has ever preserved is a Tupperware experiment from 2019."
)

OUTPUT_PATH = "/output/entry.txt"


def validate(text):
    """Check the entry against the competition gate."""
    if not text or not text.strip():
        return "entry is empty or only whitespace"
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    if not 1 <= len(text) <= 200:
        return "entry must be 1-200 characters, got %d" % len(text)
    return None


def validate_entry(path):
    """Re-read the written entry from disk and re-validate the gate.

    Reads the file as raw bytes, decodes as UTF-8, and requires the
    content to be byte-for-byte identical to the expected entry, then
    re-runs the same gate checks (1-200 chars, single line, non-blank).
    """
    with open(path, "rb") as f:
        raw = f.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return "entry.txt is not valid UTF-8"
    if raw != ENTRY.encode("utf-8"):
        return "entry.txt differs from the expected entry"
    error = validate(text)
    if error:
        return "re-validation failed: %s" % error
    return None


def main():
    error = validate(ENTRY)
    if error:
        print("INVALID: %s" % error, file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(ENTRY)
    error = validate_entry(OUTPUT_PATH)
    if error:
        print("INVALID: %s" % error, file=sys.stderr)
        return 1
    print("Wrote %d characters to %s" % (len(ENTRY), OUTPUT_PATH))
    print(ENTRY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
