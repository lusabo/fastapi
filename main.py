from fastapi import FastAPI, Body, HTTPException

from models import Theme, Question, Assessment, Answer
from services import GroqService

app = FastAPI(
    title="API de Educação e E-learning",
    description="API que fornece serviços de IA para geração de questões e análise de respostas.",
    version="1.0.0",
    author="Luciano Borges, Marcio Hernandez e Gustavo Menossi"
)


@app.post("/api/v1/generate-question",
          response_model=Question,
          summary="Geração de questão por tema")
def generate_question(payload: Theme = Body(..., description="Tema para a geração da questão")):
    # Validação adicional (opcional)
    if not payload.theme.strip():
        raise HTTPException(status_code=422, detail="O tema não pode ser vazio.")

    service = GroqService()
    question = service.create_question(payload.theme)
    return Question(question=question)


@app.post("/api/v1/analyze-response",
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
