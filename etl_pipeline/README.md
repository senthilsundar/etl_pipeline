# Random User ETL + dbt Pipeline

This repository implements the supplied assessment specification.

## What is included

- Python ETL using an abstract `BaseDataSource` and concrete `RandomUserAPIDataSource` / `FileDataSource`.
- Composition-based `IngestionPipeline` with fetcher, transformer, validator and writer.
- Vectorized pandas transformation (no row-by-row transformation loops), including forcing every `state` to `Alabama`.
- Strict Pydantic v2 validation for name, gender, location, email, age and registration date.
- Raw JSON and cleaned CSV outputs.
- Unit tests for transformer, validator and writer, plus a mocked API test and end-to-end pipeline test.
- dbt project with seed, staging, enriched intermediate model, incremental `dim_users`, schema/custom tests, and `top_3_recent_users_per_state` view.

## Data note

`data/offline_source.json` is a deterministic 1,000-row RandomUser-shaped fixture included to make the submission reproducible in offline environments. The production source class still calls `https://randomuser.me/api/` and requests the configured row count. `data/raw_users.json` and `data/clean_users.csv` were generated from that offline fixture in this packaged submission.

## Run the ETL

```bash
python -m pip install -e '.[dev]'
python -m etl_pipeline.cli --limit 1000 --output-dir data
```

For an offline/reproducible run:

```bash
python -m etl_pipeline.cli --limit 1000 --source-file data/offline_source.json --output-dir data
```

## Run tests and coverage

```bash
pytest
```

The pytest configuration fails the run if coverage is below 85%.

## Run dbt

```bash
cd dbt_user_pipeline
DBT_PROFILES_DIR=. dbt seed
DBT_PROFILES_DIR=. dbt run
DBT_PROFILES_DIR=. dbt test
```

The model flow is:

`clean_users (seed) -> stg_users -> int_users_enriched -> dim_users -> top_3_recent_users_per_state`

`dim_users` is incremental with `email` as the unique key. On incremental runs, it only emits new users or users whose incoming registration timestamp is newer than the current dimensional record; `delete+insert` therefore gives SCD Type 1 replacement behavior. Inside each incremental batch, `row_number()` keeps the latest record per email.
