from pydantic import BaseModel, Field


class Answer(BaseModel):
    answer: str = Field(..., min_length=1, description="Resposta fornecida pelo usuário")
