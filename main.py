#!/usr/bin/env python3
"""Write one deadpan weather forecast to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The forecast is a
fixed string. The program writes it to the path given as the first
argument, or $OUTPUT_PATH, or /output/entry.txt by default, and enforces
the competition gate: 1 to 160 characters, not only white space.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

FORECAST = "In Dullmere, a high of 11 degrees, a low of 10, and drizzle that has been falling since 2019. Locals no longer notice. Visitors are issued towels on arrival."

MIN_CHARS = 1
MAX_CHARS = 160
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 160 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"forecast is {chars} characters, outside 1-160")
    if not text.strip():
        raise ValueError("forecast is only white space")
    return chars


def write_entry(path: Path, text: str) -> int:
    """Validate the text, write it to path, and return its length.

    Creates any missing parent directories first.
    """
    chars = validate(text)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return chars


def main() -> int:
    path = resolve_output_path()
    try:
        chars = write_entry(path, FORECAST)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
