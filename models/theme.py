from pydantic import BaseModel, Field


class Theme(BaseModel):
    """
    A Pydantic model representing a theme for generating questions.
    """
    theme: str = Field(..., description="Tema para a geração das questões")