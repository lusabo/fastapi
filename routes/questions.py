# app/routes/questions.py
from fastapi import APIRouter, Body, HTTPException, Depends

from models import Theme, Question, Assessment, Answer
from routes.auth import get_current_user
from services.groq_service import GroqService

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post("/generate-question",
             response_model=Question,
             summary="Geração de questão por tema")
def generate_question(
        payload: Theme = Body(..., description="Tema para a geração da questão")  # Endpoint protegido
):
    if not payload.theme.strip():
        raise HTTPException(status_code=422, detail="O tema não pode ser vazio.")

    service = GroqService()
    question_text = service.create_question(payload.theme)
    return Question(question=question_text)


@router.post("/analyze-response",
             response_model=Assessment,
             summary="Análise de resposta")
def analyze_response(
        question: Question = Body(..., description="Objeto contendo a questão"),
        answer: Answer = Body(..., description="Objeto contendo a resposta")
):
    if not question.question.strip():
        raise HTTPException(status_code=422, detail="A questão não pode ser vazia.")
    if not answer.answer.strip():
        raise HTTPException(status_code=422, detail="A resposta não pode ser vazia.")

    service = GroqService()
    assessment = service.analyze_response(question.question, answer.answer)
    return assessment
