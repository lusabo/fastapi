# FastAPI - Construção de APIs para Inteligência Artificial

![FastAPI](https://img.shields.io/badge/FastAPI-0.115.8-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)

### Universidade Federal de Goiás
### Pós-Graduação em Sistemas e Agentes Inteligentes
### Disciplina: Construção de APIs para Inteligência Artificial

### Professor
* Rogério Rodrigues

### Alunos
* Luciano Borges
* Gustavo Menossi
* Marcio Hernandez

Este projeto foi desenvolvido para a disciplina **Construção de APIs para Inteligência Artificial** do programa de Pós-Graduação em Sistemas e Agentes Inteligentes da Universidade Federal de Goiás. O objetivo é criar uma API robusta utilizando o framework **FastAPI**.

## 📌 Funcionalidades
- Estrutura modular com **models**, **routes** e **services**.
- Validação de dados utilizando **Pydantic**.
- Documentação automática da API com **Swagger** e **Redoc**.
- Configuração de ambiente utilizando **dotenv**.
- Persistência de dados com banco de dados (SQLite, PostgreSQL ou outro configurado).

## 📁 Estrutura do Projeto
```bash
fastapi/
│── app/
│   ├── models/        # Modelos de dados com Pydantic
│   ├── routes/        # Endpoints da API
│   ├── services/      # Lógica de negócio
│── main.py            # Programa principal
│── .env-sample        # Exemplo de variáveis de ambiente
│── requirements.txt   # Dependências do projeto
│── README.md          # Documentação
│── .gitignore         # Arquivos ignorados pelo Git
```

## 🚀 Tecnologias Utilizadas
- **FastAPI** - Framework para criação de APIs de alto desempenho.
- **Pydantic** - Validação e serialização de dados.
- **Uvicorn** - Servidor ASGI de alto desempenho.
- **Dotenv** - Gerenciamento de variáveis de ambiente.

## 🔧 Configuração do Ambiente
### Orientações para executar a API
Sugestão de versão do Python: **3.10 ou superior**

1. **Crie um ambiente virtual**
```bash
python -m venv env
```

2. **Ative o ambiente virtual**
- No Windows:
```bash
env\Scripts\activate
```
- No Linux/macOS:
```bash
source env/bin/activate
```

3. **Instale a última versão do pip**
```bash
python.exe -m pip install --upgrade pip
```

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

5. **Renomeie o arquivo `.env.sample` para `.env` e preencha as variáveis de ambiente**
```bash
mv .env-sample .env
```

6. **Execute o pacote padrão do FastAPI**
```bash
pip install fastapi[standard]
```

7. **Executar a API em ambiente de desenvolvimento**
```bash
fastapi dev main.py
```

## 📖 Documentação Automática
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🛠 Autenticação
1. **Acesse o botão `Authorize`**.
2. **Informe as credenciais**:
   - **Username**: `admin`
   - **Password**: `admin`
3. **Gere o token na API AUTH**.
4. **Utilize o `access_token` gerado para autenticação na API** via `GET /auth/users/me`.

---

📌 Desenvolvido por **Luciano Borges, Gustavo Menossi e Marcio Hernandez** para a Pós-Graduação em Sistemas e Agentes Inteligentes - UFG.

