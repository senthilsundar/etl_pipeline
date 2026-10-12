from __future__ import annotations

import pytest


@pytest.fixture
def api_record() -> dict:
    return {
        "gender": "female",
        "name": {"title": "Ms", "first": "Ada", "last": "Lovelace"},
        "location": {"city": "London", "state": "Greater London", "country": "United Kingdom"},
        "email": "ADA@example.com",
        "dob": {"age": 36},
        "registered": {"date": "2024-01-02T03:04:05.000Z"},
    }
