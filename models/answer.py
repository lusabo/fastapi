from pydantic import BaseModel


class Answer(BaseModel):
    answer: str
