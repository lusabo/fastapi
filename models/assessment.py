from pydantic import BaseModel


class Assessment(BaseModel):
    feedback: str
    score: str
