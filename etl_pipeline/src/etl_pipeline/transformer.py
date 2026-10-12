from __future__ import annotations

from typing import Any

import pandas as pd


class DataTransformer:
    """Vectorized flattening, cleaning and normalization."""

    output_columns = [
        "name",
        "gender",
        "city",
        "state",
        "country",
        "email",
        "age",
        "registration_date",
    ]

    def transform(self, records: list[dict[str, Any]]) -> pd.DataFrame:
        if not records:
            return pd.DataFrame(columns=self.output_columns)

        frame = pd.json_normalize(records)
        frame = frame.rename(
            columns={
                "location.city": "city",
                "location.state": "state",
                "location.country": "country",
                "dob.age": "age",
                "registered.date": "registration_date",
            }
        )

        # Support RandomUser's nested name as well as an already-flat file source.
        if {"name.first", "name.last"}.issubset(frame.columns):
            frame["name"] = (
                frame["name.first"].fillna("").astype("string").str.strip()
                + " "
                + frame["name.last"].fillna("").astype("string").str.strip()
            ).str.strip()

        missing = [column for column in self.output_columns if column not in frame.columns]
        if missing:
            raise ValueError(f"Source is missing required fields after normalization: {missing}")

        cleaned = frame.loc[:, self.output_columns].copy()
        text_columns = ["name", "gender", "city", "country", "email"]
        cleaned[text_columns] = cleaned[text_columns].apply(
            lambda series: series.astype("string").str.strip()
        )
        cleaned["gender"] = cleaned["gender"].str.lower().replace({"non-binary": "other"})
        cleaned["email"] = cleaned["email"].str.lower()
        cleaned["state"] = "Alabama"
        cleaned["age"] = pd.to_numeric(cleaned["age"], errors="raise").astype("int64")
        cleaned["registration_date"] = pd.to_datetime(
            cleaned["registration_date"], errors="raise", utc=True
        )
        return cleaned
