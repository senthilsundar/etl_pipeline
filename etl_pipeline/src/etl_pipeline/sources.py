from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import pandas as pd
import requests


class BaseDataSource(ABC):
    """Abstract contract for ingestion sources."""

    @abstractmethod
    def fetch(self, limit: int) -> list[dict[str, Any]]:
        """Return at most *limit* source records."""
        raise NotImplementedError


class RandomUserAPIDataSource(BaseDataSource):
    """Fetch user records from randomuser.me."""

    def __init__(self, base_url: str = "https://randomuser.me/api/", timeout_seconds: int = 30):
        self.base_url = base_url
        self.timeout_seconds = timeout_seconds

    def fetch(self, limit: int) -> list[dict[str, Any]]:
        if limit <= 0:
            return []
        response = requests.get(
            self.base_url,
            params={"results": limit, "noinfo": ""},
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        payload = response.json()
        results = payload.get("results")
        if not isinstance(results, list):
            raise ValueError("Random User API response did not contain a results list")
        return results[:limit]


class FileDataSource(BaseDataSource):
    """Read local JSON or CSV data for reproducible/offline runs."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def fetch(self, limit: int) -> list[dict[str, Any]]:
        if limit <= 0:
            return []
        suffix = self.path.suffix.lower()
        if suffix == ".json":
            with self.path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
            records = payload.get("results", payload) if isinstance(payload, dict) else payload
            if not isinstance(records, list):
                raise ValueError("JSON source must be a list or contain a 'results' list")
            return records[:limit]
        if suffix == ".csv":
            return pd.read_csv(self.path).head(limit).to_dict(orient="records")
        raise ValueError(f"Unsupported file type: {suffix}")
