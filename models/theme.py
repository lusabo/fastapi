from pydantic import BaseModel, Field


class Theme(BaseModel):
    theme: str = Field(..., min_length=1, max_length=20, description="Nome do tema")
