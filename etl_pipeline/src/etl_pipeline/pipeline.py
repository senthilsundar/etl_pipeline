from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .sources import BaseDataSource
from .transformer import DataTransformer
from .validator import DataValidator
from .writer import DataWriter


@dataclass(frozen=True)
class PipelineResult:
    raw_path: Path
    clean_path: Path
    row_count: int


class IngestionPipeline:
    """Composition-based ETL orchestration."""

    def __init__(
        self,
        source: BaseDataSource,
        transformer: DataTransformer,
        validator: DataValidator,
        writer: DataWriter,
    ):
        self.source = source
        self.transformer = transformer
        self.validator = validator
        self.writer = writer

    def run(self, limit: int = 1000) -> PipelineResult:
        raw_records = self.source.fetch(limit)
        raw_path = self.writer.write_raw(raw_records)
        transformed: pd.DataFrame = self.transformer.transform(raw_records)
        validated = self.validator.validate(transformed)
        clean_path = self.writer.write_clean(validated)
        return PipelineResult(raw_path=raw_path, clean_path=clean_path, row_count=len(validated))
