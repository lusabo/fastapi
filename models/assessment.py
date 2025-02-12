from pydantic import BaseModel, Field, field_validator


class Assessment(BaseModel):
    feedback: str = Field(..., description="Feedback da análise da resposta")
    score: str = Field(..., description="Score em percentual")

    @field_validator("feedback", mode="before")
    def strip_feedback(self, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("score", mode="before")
    def strip_score(self, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value
