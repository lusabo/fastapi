from pydantic import BaseModel, Field, field_validator


class Theme(BaseModel):
    theme: str = Field(..., min_length=1, max_length=20, description="Nome do tema")

    @field_validator("theme", mode="before")
    def strip_whitespace(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value
