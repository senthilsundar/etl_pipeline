from __future__ import annotations

import pandas as pd
from pydantic import ValidationError

from .models import UserRecord


class DataValidator:
    """Validate every transformed record against the strict Pydantic schema."""

    def validate(self, frame: pd.DataFrame) -> pd.DataFrame:
        records = frame.to_dict(orient="records")
        errors: list[str] = []
        for index, record in enumerate(records):
            # Pandas Timestamp is a datetime subclass; int64 needs normalizing to Python int.
            normalized = dict(record)
            normalized["age"] = int(normalized["age"])
            try:
                UserRecord.model_validate(normalized)
            except ValidationError as exc:
                errors.append(f"row {index}: {exc}")
        if errors:
            raise ValueError("Schema validation failed:\n" + "\n".join(errors))
        return frame
