#!/usr/bin/env python
"""Entry‑point so the project can be started via `python -m got_survival`."""
from __future__ import annotations

from pathlib import Path
import argparse

from .pipeline import load_data, run_experiment


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="got_survival", description="Train GOT survival models from the CLI"
    )
    parser.add_argument("csv", type=Path, help="Path to raw Game‑of‑Thrones CSV file")
    args = parser.parse_args()

    X, y = load_data(args.csv)
    run_experiment(X, y)


if __name__ == "__main__":
    main()