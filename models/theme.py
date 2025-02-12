from pydantic import BaseModel, Field, field_validator


class Theme(BaseModel):
    """
    Modelo que representa um tema.

    Atributos:
        theme (str): Nome do tema, deve ter entre 1 e 20 caracteres.
    """
    theme: str = Field(..., min_length=1, max_length=20, description="Nome do tema")

    @field_validator("theme", mode="before")
    def strip_whitespace(cls, value: str) -> str:
        """
        Validador que remove espaços em branco do início e do fim do valor do tema.

        Args:
            value (str): Valor do tema.

        Returns:
            str: Valor do tema sem espaços em branco no início e no fim.
        """
        if isinstance(value, str):
            return value.strip()
        return value
