from fastapi import FastAPI, Body

from models import Theme, Question
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
    service = GroqService()
    question = service.create_question(payload.theme)
    return Question(question=question)
