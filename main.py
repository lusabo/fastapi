from fastapi import FastAPI, Body

from models import Theme, Question

app = FastAPI(
    title="API de Educação e E-learning",
    description="API que fornece serviços de IA para geração de questões e análise de respostas.",
    version="1.0.0"
)


@app.post("/api/v1/generate-question",
          response_model=Question,
          summary="Geração de questão por tema")
def generate_question(payload: Theme = Body(..., description="Tema para a geração da questão")):
    if payload.theme == "geografia":
        question = Question(question="Qual a capital do Brasil?")
    else:
        question = Question(question="Qual a capital da Argentina?")
    return question
