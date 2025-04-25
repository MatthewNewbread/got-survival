"""
Lightweight training pipeline for predicting character survival in "Game of Thrones".

Usage:
    python pipeline.py data/game_of_thrones_train.csv

The script performs:
1. Data loading & feature engineering
2. Train/test split
3. Model training (LogReg & RandomForest in scalable pipelines)
4. Evaluation with a concise classification report

Add or swap models in `build_pipelines()` – the rest of the code stays unchanged.
"""
from __fututre__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

RANDOM_STATE = 42
TEST_SIZE = 0.2

# ---------------------------------------------------------------------------
# 1. Data loading & basic feature engineering
# ---------------------------------------------------------------------------

def load_data(csv_path: str | Path):
    """Return features *X* and target *y* from the raw CSV file."""
    df = pd.read_csv(csv_path, index_col='S.No')

    numeric = ['age', 'dateOfBirth']
    df[numeric] = df[numeric].fillna(df[numeric].median())

    df["isPopular"] = (df["popularity"] > 0.5).astype(int)
    df["boolDeadRelations"] = (df["numDeadRelations"] > 0).astype(int)

    drop = [
        "name",
        "title",
        "culture",
        "mother",
        "father",
        "heir",
        "house",
        "spouse",
        "isAliveSpouse",
        "isAliveMother",
        "isAliveFather",
        "isAliveHeir",
        "numDeadRelations",
        "popularity",
    ]

    X = df.drop(columns=["isAlive", *drop])
    y = df["isAlive"]
    return X, y

# ---------------------------------------------------------------------------
# 2. Build preprocessing + model pipelines
# ---------------------------------------------------------------------------

def build_pipelines() -> dict[str, Pipeline]:
    numeric = ["age", "dateOfBirth"]
    categorical = ["male", "isMarried", "isNoble", "isPopular", "boolDeadRelations"]

    preprocessor = ColumnTransformer(
        [
            ("num", StandardScaler(), numeric),
            ("cat", "passthrough", categorical),
        ]
    )

    models = {
        "log_reg": LogisticRegression(max_iter=1000, n_jobs=-1, random_state=RANDOM_STATE),
        "rf": RandomForestClassifier(n_estimators=300, random_state=RANDOM_STATE),
    }

    return {name: Pipeline([("prep", preprocessor), ("clf", model)]) for name, model in models.items()}

# ---------------------------------------------------------------------------
# 3. Train, evaluate, and print a minimal report
# ---------------------------------------------------------------------------

def run_experiment(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE
    )

    for name, pipeline in build_pipelines().items():
        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_test)
        print("\n" + "-" * 60)
        print(f"Model: {name}")
        print(classification_report(y_test, preds, digits=3))

def main():
    parser = argparse.ArgumentParser(description="Train GOT survival models")
    parser.add_argument("csv", help="Path to training CSV file")
    args = parser.parse_args()

    X, y = load_data(args.csv)
    run_experiment(X, y)
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    X_train.to_csv("data/processed/train.csv", index=False)
    X_test.to_csv("data/processed/test.csv",  index=False)

if __name__ == "__main__":
    main()
