from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


class DataWriter:
    """Write raw JSON and cleaned CSV output."""

    def __init__(self, output_dir: str | Path):
        self.output_dir = Path(output_dir)

    def write_raw(self, records: list[dict[str, Any]], filename: str = "raw_users.json") -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        target = self.output_dir / filename
        target.write_text(json.dumps(records, indent=2, default=str), encoding="utf-8")
        return target

    def write_clean(self, frame: pd.DataFrame, filename: str = "clean_users.csv") -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        target = self.output_dir / filename
        frame.to_csv(target, index=False)
        return target
