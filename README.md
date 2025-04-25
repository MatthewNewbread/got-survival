🏰 Game of Thrones — Survival Prediction

Predict whether a character from A Song of Ice and Fire will stay alive based on their attributes.

📂 Project structure

got-survival/
├ data/
│   ├ raw/                # original full‑size CSVs (ignored by Git)
│   ├ processed/          # train/test splits saved by the pipeline
│   └ sample/             # light demo dataset that *is* tracked in Git
├ src/
│   ├ pipeline.py         # training & evaluation script
│   ├ viz.py              # quick visualisations
│   ├ __init__.py         # makes `src` an importable package
│   └ __main__.py         # allows `python -m got_survival ...`
├ tests/                  # pytest-based sanity checks
├ requirements.txt        # project dependencies (see below)
├ README.md               # ← you are here
├ .gitignore              # files to exclude from version control
└ LICENSE

🚀 Quickstart

git clone https://github.com/yourname/got-survival.git
cd got-survival
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# train two baseline models and print a classification report
python src/pipeline.py data/raw/game_of_thrones.csv

Visualisations

python src/viz.py data/raw/game_of_thrones.csv --target-dist --heatmap

🛠️ Data preparation

Full dataset → place in data/raw/.Example: data/raw/game_of_thrones.csv (ignored by Git).

Training pipeline reads the raw path you pass on the command line and automatically writes processed splits into data/processed/.

Sample dataset (optional) — create a light subset for PRs & CI:

python scripts/make_sample.py data/raw/game_of_thrones.csv
# → data/sample/sample.csv (tracked by Git, only ~200 rows)

📦 Dependencies (requirements.txt)

Minimal versions known to work:

pandas>=2.0
numpy>=1.26
scikit-learn>=1.5
matplotlib>=3.9
seaborn>=0.13

Freeze only what you import directly; transitive packages will be pulled automatically.Pin exact versions (==) later, e.g. when you start CI or need reproducibility.

🤖 Tests

pytest -q

The smoke‑test in tests/test_pipeline.py just make sure the pipeline runs end‑to‑end on the small sample.

📜 License

MIT