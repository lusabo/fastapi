from fastapi.testclient import TestClient

from main import app
# Para facilitar os testes dos endpoints que dependem do usuário autenticado,
# sobrescrevemos a dependência get_current_user.
from routes.auth_routes import get_current_user
from services import auth_service


def override_get_current_user():
    return {"id": "test-user"}


app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


# ---------- Testes para /auth/token e /auth/users/me ----------

def test_auth_token_success(monkeypatch):
    def fake_verify_user(username, password):
        return {"id": "test-user", "username": username}

    def fake_create_access_token(data, expires_delta=None):
        return "fake-token"

    monkeypatch.setattr(auth_service, "verify_user", fake_verify_user)
    monkeypatch.setattr(auth_service, "create_access_token", fake_create_access_token)

    response = client.post("/auth/token", data={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == "fake-token"
    assert data["token_type"] == "bearer"


def test_auth_token_failure(monkeypatch):
    def fake_verify_user(username, password):
        return None

    monkeypatch.setattr(auth_service, "verify_user", fake_verify_user)
    response = client.post("/auth/token", data={"username": "errado", "password": "errado"})
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Usuário ou senha incorretos"


def test_read_users_me():
    response = client.get("/auth/users/me", headers={"Authorization": "Bearer fake-token"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "test-user"


# ---------- Testes para endpoints de Questions ----------

# Helpers para simular o GroqService
def fake_create_question(self, theme):
    # Retorna a string com o tema "trimmed"
    return f"Pergunta gerada para {theme.strip()}"


def fake_create_question_fail(self, theme):
    raise Exception("Falha na geração da pergunta")


def fake_analyze_response(self, question, answer):
    from models.assessment import Assessment
    return Assessment(score="90%", feedback="Resposta quase correta.")


def fake_analyze_response_fail(self, question, answer):
    raise Exception("Falha na análise da resposta")


def test_generate_question_success(monkeypatch):
    from services.groq_service import GroqService
    monkeypatch.setattr(GroqService, "create_question", fake_create_question)
    payload = {"theme": " História "}
    response = client.post(
        "/questions/v1/generate-question",
        json=payload,
        headers={"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 200
    data = response.json()
    # Note que o theme é "Historia" sem espaços
    assert data["question"] == "Pergunta gerada para História"


def test_generate_question_empty_theme():
    payload = {"theme": "   "}
    response = client.post(
        "/questions/v1/generate-question",
        json=payload,
        headers={"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["msg"] == "String should have at least 1 character"


def test_generate_question_internal_error(monkeypatch):
    from services.groq_service import GroqService
    monkeypatch.setattr(GroqService, "create_question", fake_create_question_fail)
    payload = {"theme": "Matemática"}
    response = client.post(
        "/questions/v1/generate-question",
        json=payload,
        headers={"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 500


def test_generate_question_v2_success(monkeypatch):
    from services.groq_service import GroqService
    monkeypatch.setattr(GroqService, "create_question", fake_create_question)
    payload = {"theme": " Química ", "quantity": 3}
    response = client.post(
        "/questions/v2/generate-question",
        json=payload,
        headers={"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3
    for item in data:
        assert "question" in item
        assert item["question"] == "Pergunta gerada para Química"


def test_generate_question_v2_empty_theme():
    payload = {"theme": "   ", "quantity": 3}
    response = client.post(
        "/questions/v2/generate-question",
        json=payload,
        headers={"Authorization": "Bearer fake-token"}
    )
    # O endpoint deverá retornar 422 para tema vazio
    assert response.status_code == 422


def test_generate_question_v2_internal_error(monkeypatch):
    from services.groq_service import GroqService
    monkeypatch.setattr(GroqService, "create_question", fake_create_question_fail)
    payload = {"theme": "Biologia", "quantity": 2}
    response = client.post(
        "/questions/v2/generate-question",
        json=payload,
        headers={"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 500


def test_analyze_response_success(monkeypatch):
    from services.groq_service import GroqService
    monkeypatch.setattr(GroqService, "analyze_response", fake_analyze_response)
    payload = {
        "question": {"question": "Qual a fórmula da água?"},
        "answer": {"answer": "H2O"}
    }
    response = client.post(
        "/questions/v1/analyze-response",
        json=payload,
        headers={"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == "90%"
    assert data["feedback"] == "Resposta quase correta."


def test_analyze_response_empty_question():
    payload = {
        "question": {"question": "   "},
        "answer": {"answer": "Alguma resposta"}
    }
    response = client.post(
        "/questions/v1/analyze-response",
        json=payload,
        headers={"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["msg"] == "String should have at least 5 characters"


def test_analyze_response_empty_answer():
    payload = {
        "question": {"question": "Qual a fórmula da água?"},
        "answer": {"answer": "   "}
    }
    response = client.post(
        "/questions/v1/analyze-response",
        json=payload,
        headers={"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["msg"] == "String should have at least 1 character"


def test_analyze_response_internal_error(monkeypatch):
    from services.groq_service import GroqService
    monkeypatch.setattr(GroqService, "analyze_response", fake_analyze_response_fail)
    payload = {
        "question": {"question": "Qual a fórmula da água?"},
        "answer": {"answer": "H2O"}
    }
    response = client.post(
        "/questions/v1/analyze-response",
        json=payload,
        headers={"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 500
