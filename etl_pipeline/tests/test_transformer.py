from etl_pipeline.transformer import DataTransformer


def test_transformer_flattens_and_normalizes(api_record):
    frame = DataTransformer().transform([api_record])
    assert list(frame.columns) == DataTransformer.output_columns
    assert frame.loc[0, "name"] == "Ada Lovelace"
    assert frame.loc[0, "email"] == "ada@example.com"
    assert frame.loc[0, "state"] == "Alabama"
    assert int(frame.loc[0, "age"]) == 36
    assert str(frame.loc[0, "registration_date"].tz) == "UTC"


def test_transformer_empty():
    assert DataTransformer().transform([]).empty


def test_transformer_rejects_missing_fields(api_record):
    del api_record["email"]
    try:
        DataTransformer().transform([api_record])
    except ValueError as exc:
        assert "missing required fields" in str(exc).lower()
    else:
        raise AssertionError("Expected missing-field validation")
