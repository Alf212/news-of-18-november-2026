#!/usr/bin/env python3
"""Entry program for make.fun's news-image-20261118 contest.

The entry image is entry.png, held beside this file in the repository
(drawn by compose.py). This program's whole job is to place those exact
bytes at the harness's output path: it copies entry.png to
$MAKEFUN_OUTPUT_DIR/entry.png, or to /output/entry.png when the variable
is unset (the grader's container). Standard library only, no network,
and the same bytes every run, as the harness requires.

Local check:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def checked_source() -> Path:
    """Fail loudly rather than submit a truncated or wrong asset."""
    with SOURCE.open("rb") as fh:
        if fh.read(8) != PNG_SIGNATURE:
            raise SystemExit(f"{SOURCE.name} is not a PNG file")
    return SOURCE


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(checked_source(), out_dir / "entry.png")


if __name__ == "__main__":
    main()
