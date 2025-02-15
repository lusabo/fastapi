import json
import pytest
from datetime import timedelta

import jwt

from pydantic import ValidationError


# ===== Testes para services/auth_service.py =====

def test_create_access_token_success(monkeypatch):
    from services.auth_service import create_access_token

    # Define as variáveis de ambiente necessárias para o teste.
    monkeypatch.setenv("SECRET_KEY", "testsecret")
    monkeypatch.setenv("ALGORITHM", "HS256")

    data = {"sub": "123"}
    token = create_access_token(data, expires_delta=timedelta(minutes=1))
    decoded = jwt.decode(token, "testsecret", algorithms=["HS256"])
    assert decoded["sub"] == "123"
    assert "exp" in decoded


def test_create_access_token_failure(monkeypatch):
    from services.auth_service import create_access_token

    # Remove as variáveis de ambiente para simular erro
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("ALGORITHM", raising=False)

    data = {"sub": "123"}
    with pytest.raises(ValueError):
        create_access_token(data)


def test_verify_user_success():
    from services.auth_service import verify_user
    user = verify_user("admin", "admin")
    assert user["id"] == "123"


def test_verify_user_failure():
    from services.auth_service import verify_user
    assert verify_user("usuario", "senhaerrada") is None


# ===== Testes para services/groq_service.py =====

# Helper para simular as respostas do client do Groq
class DummyCompletion:
    class DummyChoice:
        def __init__(self, content):
            self.message = type("DummyMessage", (), {"content": content})
    def __init__(self, content):
        self.choices = [self.DummyChoice(content)]


def dummy_create_completion_success(messages, model):
    return DummyCompletion("Pergunta de teste")


def dummy_create_completion_fail(messages, model):
    raise Exception("Erro na API Groq")


def dummy_create_completion_analysis(messages, model):
    # Retorna uma string JSON válida
    response = '{"score": "80%", "feedback": "Bom trabalho."}'
    return DummyCompletion(response)


def dummy_create_completion_invalid_json(messages, model):
    return DummyCompletion("texto não-json")


def test_groq_service_init_failure(monkeypatch):
    from services.groq_service import GroqService
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with pytest.raises(ValueError):
        GroqService()


def test_groq_service_create_question_success(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "dummy_key")
    from services.groq_service import GroqService
    service = GroqService()
    monkeypatch.setattr(service.client.chat.completions, "create", dummy_create_completion_success)
    question_text = service.create_question("Teste")
    assert question_text == "Pergunta de teste"


def test_groq_service_create_question_failure(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "dummy_key")
    from services.groq_service import GroqService
    service = GroqService()
    monkeypatch.setattr(service.client.chat.completions, "create", dummy_create_completion_fail)
    with pytest.raises(Exception) as excinfo:
        service.create_question("Teste")
    assert "Erro interno ao gerar a pergunta." in str(excinfo.value)


def test_groq_service_analyze_response_success(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "dummy_key")
    from services.groq_service import GroqService
    service = GroqService()
    monkeypatch.setattr(service.client.chat.completions, "create", dummy_create_completion_analysis)
    assessment = service.analyze_response("Pergunta", "Resposta")
    assert assessment.score == "80%"
    assert assessment.feedback == "Bom trabalho."


def test_groq_service_analyze_response_failure(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "dummy_key")
    from services.groq_service import GroqService
    service = GroqService()
    monkeypatch.setattr(service.client.chat.completions, "create", dummy_create_completion_fail)
    with pytest.raises(Exception) as excinfo:
        service.analyze_response("Pergunta", "Resposta")
    assert "Erro interno ao analisar a resposta." in str(excinfo.value)


def test_groq_service_analyze_response_invalid_json(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "dummy_key")
    from services.groq_service import GroqService
    service = GroqService()
    monkeypatch.setattr(service.client.chat.completions, "create", dummy_create_completion_invalid_json)
    with pytest.raises(ValueError) as excinfo:
        service.analyze_response("Pergunta", "Resposta")
    assert "Resposta em formato inválido." in str(excinfo.value)
