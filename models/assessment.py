from pydantic import BaseModel, Field, field_validator


class Assessment(BaseModel):
    """
    Modelo que representa uma avaliação.

    Atributos:
        feedback (str): Feedback da análise da resposta.
        score (str): Score em percentual.
    """

    feedback: str = Field(..., description="Feedback da análise da resposta")
    score: str = Field(..., description="Score em percentual")

    @field_validator("feedback", mode="before")
    def strip_feedback(cls, value: str) -> str:
        """
        Validador para remover espaços em branco do feedback.

        Args:
            value (str): O valor do feedback.

        Returns:
            str: O valor do feedback sem espaços em branco.
        """
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("score", mode="before")
    def strip_score(cls, value: str) -> str:
        """
        Validador para remover espaços em branco do score.

        Args:
            value (str): O valor do score.

        Returns:
            str: O valor do score sem espaços em branco.
        """
        if isinstance(value, str):
            return value.strip()
        return value
