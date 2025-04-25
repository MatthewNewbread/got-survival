#!/usr/bin/env python
"""
Visualization helpers for the Game‑of‑Thrones survival project.

Run examples
------------
$ python viz.py data/raw/game_of_thrones.csv --heatmap
$ python viz.py data/raw/game_of_thrones.csv --target-dist

This script is intentionally thin: heavy EDA belongs in notebooks, while here we
keep just a couple of production‑ready plots that stakeholders often ask for.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from pipeline import load_data

sns.set_theme(context="talk", style="whitegrid")

# ---------------------------------------------------------------------------
# Plotting functions
# ---------------------------------------------------------------------------

def target_distribution(y: pd.Series, *, title: str = "Target distribution") -> None:
    """Pie chart Dead vs Alive."""
    counts = y.value_counts().reindex([0, 1])
    counts.plot.pie(autopct="%1.1f%%", labels=["Dead", "Alive"], figsize=(6, 6))
    plt.title(title)
    plt.ylabel("")
    plt.show()


def correlation_heatmap(df: pd.DataFrame, *, title: str = "Correlation matrix") -> None:
    """Annotated heatmap of Pearson correlations."""
    plt.figure(figsize=(12, 10))
    sns.heatmap(df.corr(), cmap="coolwarm", annot=True, fmt=".2f")
    plt.title(title)
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(description="Quick visualisations for GOT data")
    p.add_argument("csv", type=Path, help="Path to raw CSV file")
    p.add_argument("--heatmap", action="store_true", help="Correlation heatmap")
    p.add_argument("--target-dist", action="store_true", help="Distribution of isAlive")
    return p.parse_args()

def main():
    args = parse_args()
    X, y = load_data(args.csv)
    df = pd.concat([X, y.rename("isAlive")], axis=1)

    if args.target_dist:
        target_distribution(y)

    if args.heatmap:
        correlation_heatmap(df)

    if not (args.heatmap or args.target_dist):
        print("Nothing to do. Add --heatmap or --target-dist.")

if __name__ == "__main__":
    main()