from pydantic import BaseModel, Field


class Question(BaseModel):
    question: str = Field(..., min_length=5, description="Texto da questão gerada")