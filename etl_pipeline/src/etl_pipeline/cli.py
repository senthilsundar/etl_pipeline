from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import IngestionPipeline
from .sources import FileDataSource, RandomUserAPIDataSource
from .transformer import DataTransformer
from .validator import DataValidator
from .writer import DataWriter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the user ingestion pipeline")
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--output-dir", default="data")
    parser.add_argument("--source-file", help="Optional local JSON/CSV source instead of API")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    source = FileDataSource(args.source_file) if args.source_file else RandomUserAPIDataSource()
    pipeline = IngestionPipeline(
        source=source,
        transformer=DataTransformer(),
        validator=DataValidator(),
        writer=DataWriter(Path(args.output_dir)),
    )
    result = pipeline.run(limit=args.limit)
    print(f"Wrote {result.row_count} rows to {result.clean_path}; raw data: {result.raw_path}")


if __name__ == "__main__":
    main()
