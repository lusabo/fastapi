import pytest
from pydantic import ValidationError

from models.answer import Answer
from models.assessment import Assessment
from models.question import Question
from models.questions import Questions
from models.theme import Theme


def test_answer_strip():
    answer = Answer(answer="  uma resposta  ")
    assert answer.answer == "uma resposta"


def test_answer_min_length():
    with pytest.raises(ValidationError):
        # Como o campo answer exige min_length=1, string vazia gera erro.
        Answer(answer="")


def test_assessment_strip():
    assessment = Assessment(feedback="  Feedback bom  ", score=" 90% ")
    assert assessment.feedback == "Feedback bom"
    assert assessment.score == "90%"


def test_question_strip():
    question = Question(question="  Qual a capital do Brasil?  ")
    assert question.question == "Qual a capital do Brasil?"


def test_question_min_length():
    with pytest.raises(ValidationError):
        # Menos de 5 caracteres gera erro.
        Question(question="abc")


def test_questions_valid():
    obj = Questions(theme="  História ", quantity=3)
    assert obj.theme == "História"
    assert obj.quantity == 3


def test_questions_invalid_theme():
    # Mesmo que o tema venha com espaços, após o strip pode ficar vazio.
    with pytest.raises(ValidationError):
        Questions(theme="   ", quantity=3)


def test_questions_invalid_quantity():
    with pytest.raises(ValidationError):
        # quantity deve ser maior que 1
        Questions(theme="Geografia", quantity=1)


def test_theme_strip():
    theme = Theme(theme="  Matemática  ")
    assert theme.theme == "Matemática"


def test_theme_length():
    with pytest.raises(ValidationError):
        Theme(theme="")  # Tema com comprimento menor que 1
    with pytest.raises(ValidationError):
        Theme(theme="a" * 21)  # Tema maior que 20 caracteres
