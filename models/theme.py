from pydantic import BaseModel, Field


class Theme(BaseModel):
    theme: str
