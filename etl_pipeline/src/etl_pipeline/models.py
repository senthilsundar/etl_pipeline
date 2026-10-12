from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRecord(BaseModel):
    """Strict validated representation of a cleaned user."""

    model_config = ConfigDict(extra="forbid", strict=True)

    name: str = Field(min_length=1)
    gender: Literal["male", "female", "other"]
    city: str = Field(min_length=1)
    state: str = Field(min_length=1)
    country: str = Field(min_length=1)
    email: EmailStr
    age: int = Field(ge=0, le=120)
    registration_date: datetime
