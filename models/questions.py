from pydantic import BaseModel, Field, field_validator


class Questions(BaseModel):
    theme: str = Field(..., min_length=1, max_length=20, description="Nome do tema")
    quantity: int = Field(..., gt=1, description="Quantidade de questões a serem geradas")

    @field_validator("theme", mode="before")
    def strip_whitespace(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value
