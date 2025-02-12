from pydantic import BaseModel, Field, field_validator


class Answer(BaseModel):
    """
    Um modelo que representa uma resposta fornecida pelo utilizador.

    Attributes:
        answer (str): A resposta fornecida pelo utilizador. Deve ter um comprimento mínimo de 1.
    """
    answer: str = Field(..., min_length=1, description="Resposta fornecida pelo usuário")

    @field_validator("answer", mode="before")
    def strip_answer(cls, value: str) -> str:
        """
        Validador para remover espaços em branco iniciais e finais da resposta.

        Args:
            value (str): A resposta fornecida pelo utilizador.

        Returns:
            str: A resposta simplificada se a entrada for uma string, caso contrário, o valor original.
        """
        if isinstance(value, str):
            return value.strip()
        return value
