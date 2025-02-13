import logging
from fastapi import FastAPI
from routes import auth_routes, questions_routes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
app = FastAPI(
    title="API de Educação e E-learning",
    description=(
        "API que fornece serviços de IA para geração de questões e análise de respostas.\n\n"
        "*Equipe:* Luciano Borges, Marcio Hernandez e Gustavo Menossi\n\n"
        "*Versão:* 1.0.0\n\n"
        "*GitHub:* [GitHub](https://github.com/lusabo/fastapi)"
    ),
    version="1.0.0",
)
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(questions_routes.router, prefix="/questions", tags=["Questions"])
