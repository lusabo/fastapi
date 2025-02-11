from pydantic import BaseModel, Field, field_validator


class Question(BaseModel):
    question: str = Field(..., min_length=5, description="Texto da questão gerada")

    @field_validator("question", mode="before")
    def strip_whitespace(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value
