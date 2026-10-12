import json

import pandas as pd

from etl_pipeline.writer import DataWriter


def test_writer_outputs_raw_and_clean(tmp_path):
    writer = DataWriter(tmp_path)
    raw = [{"a": 1}]
    frame = pd.DataFrame([{"a": 1}])
    raw_path = writer.write_raw(raw)
    clean_path = writer.write_clean(frame)
    assert json.loads(raw_path.read_text()) == raw
    assert pd.read_csv(clean_path).to_dict(orient="records") == raw
