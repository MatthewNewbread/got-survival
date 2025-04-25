"""Game‑of‑Thrones survival package."""
__all__ = [
    "load_data",
    "build_pipelines",
    "run_experiment",
]

from .pipeline import load_data, build_pipelines, run_experiment  # noqa: F401

__version__ = "0.1.0"