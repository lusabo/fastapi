from pydantic import BaseModel, Field, field_validator


class Question(BaseModel):
    """
    Modelo que representa uma questão.

    Atributos:
        question (str): Texto da questão gerada. Deve ter no mínimo 5 caracteres.
    """
    question: str = Field(..., min_length=5, description="Texto da questão gerada")

    @field_validator("question", mode="before")
    def strip_whitespace(cls, value: str) -> str:
        """
        Validador que remove espaços em branco do início e do fim do texto da questão.

        Args:
            value (str): Texto da questão.

        Returns:
            str: Texto da questão sem espaços em branco no início e no fim.
        """
        if isinstance(value, str):
            return value.strip()
        return value
