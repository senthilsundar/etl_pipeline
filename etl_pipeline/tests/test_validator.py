import pandas as pd
import pytest

from etl_pipeline.validator import DataValidator


def valid_frame():
    return pd.DataFrame([
        {
            "name": "Ada Lovelace",
            "gender": "female",
            "city": "London",
            "state": "Alabama",
            "country": "United Kingdom",
            "email": "ada@example.com",
            "age": 36,
            "registration_date": pd.Timestamp("2024-01-02T03:04:05Z"),
        }
    ])


def test_validator_accepts_valid_record():
    result = DataValidator().validate(valid_frame())
    assert len(result) == 1


def test_validator_rejects_bad_age():
    frame = valid_frame()
    frame.loc[0, "age"] = 121
    with pytest.raises(ValueError, match="Schema validation failed"):
        DataValidator().validate(frame)


def test_validator_rejects_bad_email():
    frame = valid_frame()
    frame.loc[0, "email"] = "not-an-email"
    with pytest.raises(ValueError, match="Schema validation failed"):
        DataValidator().validate(frame)
