from pydantic import BaseModel, Field


class Assessment(BaseModel):
    feedback: str = Field(..., description="Feedback da análise da resposta")
    score: str = Field(..., description="Score em percentual")
