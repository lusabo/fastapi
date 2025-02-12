from pydantic import BaseModel, Field, field_validator


class Questions(BaseModel):
    """
    Modelo que representa uma pergunta.

    Atributos:
        theme (str): Nome do tema, deve ter entre 1 e 20 caracteres.
        quantity (int): Quantidade de questões a serem geradas, deve ser maior que 1.
    """
    theme: str = Field(..., min_length=1, max_length=20, description="Nome do tema")
    quantity: int = Field(..., gt=1, description="Quantidade de questões a serem geradas")

    @field_validator("theme", mode="before")
    def strip_whitespace(cls, value: str) -> str:
        """
        Remove espaços em branco do início e do fim do tema.

        Args:
            value (str): O valor do tema.

        Returns:
            str: O valor do tema sem espaços em branco.
        """
        if isinstance(value, str):
            return value.strip()
        return value
