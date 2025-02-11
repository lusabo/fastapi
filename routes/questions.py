import logging

from fastapi import APIRouter, Body, HTTPException, Depends

from models import Theme, Question, Assessment, Answer
from routes.auth import get_current_user
from services.groq_service import GroqService

logger = logging.getLogger(__name__)

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post("/generate-question",
             response_model=Question,
             summary="Geração de questão por tema")
def generate_question(
        payload: Theme = Body(..., description="Tema para a geração da questão"),
        current_user: dict = Depends(get_current_user)
):
    logger.info(f"Usuário {current_user['id']} solicitou a geração de questão para o tema: '{payload.theme}'")

    if not payload.theme.strip():
        logger.warning(f"Usuário {current_user['id']} enviou tema vazio para geração de questão.")
        raise HTTPException(status_code=422, detail="O tema não pode ser vazio.")

    service = GroqService()
    try:
        question_text = service.create_question(payload.theme)
    except Exception as e:
        logger.error(f"Erro ao gerar questão para o tema '{payload.theme}' pelo usuário {current_user['id']}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao gerar questão.")

    logger.info(f"Questão gerada com sucesso para o tema '{payload.theme}' pelo usuário {current_user['id']}.")
    return Question(question=question_text)


@router.post("/analyze-response",
             response_model=Assessment,
             summary="Análise de resposta")
def analyze_response(
        question: Question = Body(..., description="Objeto contendo a questão"),
        answer: Answer = Body(..., description="Objeto contendo a resposta"),
        current_user: dict = Depends(get_current_user)
):
    logger.info(f"Usuário {current_user['id']} solicitou a análise de resposta.")

    if not question.question.strip():
        logger.warning(f"Usuário {current_user['id']} enviou uma questão vazia.")
        raise HTTPException(status_code=422, detail="A questão não pode ser vazia.")
    if not answer.answer.strip():
        logger.warning(f"Usuário {current_user['id']} enviou uma resposta vazia.")
        raise HTTPException(status_code=422, detail="A resposta não pode ser vazia.")

    service = GroqService()
    try:
        assessment = service.analyze_response(question.question, answer.answer)
    except Exception as e:
        logger.error(
            f"Erro ao analisar resposta para a questão '{question.question}' pelo usuário {current_user['id']}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao analisar resposta.")

    logger.info(f"Análise realizada com sucesso para o usuário {current_user['id']}.")
    return assessment
