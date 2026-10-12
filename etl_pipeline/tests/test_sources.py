import json

import pandas as pd
import pytest

from etl_pipeline.sources import FileDataSource, RandomUserAPIDataSource


def test_file_data_source_json(tmp_path, api_record):
    path = tmp_path / "users.json"
    path.write_text(json.dumps([api_record, api_record]))
    assert len(FileDataSource(path).fetch(1)) == 1


def test_file_data_source_csv(tmp_path):
    path = tmp_path / "users.csv"
    pd.DataFrame([{"name": "A"}, {"name": "B"}]).to_csv(path, index=False)
    assert FileDataSource(path).fetch(1)[0]["name"] == "A"


def test_file_data_source_unsupported(tmp_path):
    path = tmp_path / "users.txt"
    path.write_text("x")
    with pytest.raises(ValueError, match="Unsupported"):
        FileDataSource(path).fetch(1)


def test_api_source_is_mocked(monkeypatch, api_record):
    class FakeResponse:
        def raise_for_status(self):
            return None
        def json(self):
            return {"results": [api_record]}

    def fake_get(*args, **kwargs):
        assert kwargs["params"]["results"] == 1
        return FakeResponse()

    monkeypatch.setattr("etl_pipeline.sources.requests.get", fake_get)
    result = RandomUserAPIDataSource().fetch(1)
    assert result == [api_record]


def test_api_rejects_malformed_response(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None
        def json(self):
            return {"results": "bad"}
    monkeypatch.setattr("etl_pipeline.sources.requests.get", lambda *a, **k: FakeResponse())
    with pytest.raises(ValueError, match="results list"):
        RandomUserAPIDataSource().fetch(1)

def test_sources_return_empty_for_non_positive_limit(tmp_path):
    path = tmp_path / "users.json"
    path.write_text("[]")
    assert FileDataSource(path).fetch(0) == []
    assert RandomUserAPIDataSource().fetch(0) == []
