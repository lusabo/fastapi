import logging
from fastapi import FastAPI
from routes import auth_route, questions_route

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
app = FastAPI(
    title="API de Educação e E-learning",
    description="API que fornece serviços de IA para geração de questões e análise de respostas.",
    version="1.0.0",
    author="Luciano Borges, Marcio Hernandez e Gustavo Menossi"
)

app.include_router(auth_route.router, prefix="/auth", tags=["Auth"])
app.include_router(questions_route.router, prefix="/questions", tags=["Questions"])
