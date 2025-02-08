from pydantic import BaseModel


class Question(BaseModel):
    """
    A model representing a question.

    Attributes:
        question (str): The text of the question.
    """
    question: str
