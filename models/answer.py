from pydantic import BaseModel, Field, Field, field_validator


class Answer(BaseModel):
    answer: str = Field(..., min_length=1, description="Resposta fornecida pelo usuário")

    @field_validator("answer", mode="before")
    def strip_answer(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value
