from etl_pipeline.pipeline import IngestionPipeline
from etl_pipeline.sources import BaseDataSource
from etl_pipeline.transformer import DataTransformer
from etl_pipeline.validator import DataValidator
from etl_pipeline.writer import DataWriter


class StubSource(BaseDataSource):
    def __init__(self, record):
        self.record = record
    def fetch(self, limit: int):
        return [self.record][:limit]


def test_pipeline_end_to_end(tmp_path, api_record):
    pipeline = IngestionPipeline(
        source=StubSource(api_record),
        transformer=DataTransformer(),
        validator=DataValidator(),
        writer=DataWriter(tmp_path),
    )
    result = pipeline.run(1)
    assert result.row_count == 1
    assert result.raw_path.exists()
    assert result.clean_path.exists()
    assert "Alabama" in result.clean_path.read_text()
