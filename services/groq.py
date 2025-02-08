import json
import os

from dotenv import load_dotenv
from groq import Groq

from models import Assessment

load_dotenv()


class GroqService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def create_question(self, theme: str):
        prompt = f"""
        Por favor, crie uma pergunta interessante e desafiadora sobre {theme}.
        A pergunta deve:
        - Ser clara, bem formulada e direta
        - Ter valor educacional
        Orientações:
        - O retorno deve ser somente a pergunta
        - O retorno não deve incluir o pensamento da LLM
        - O retorno deve ser em Português
        - O retorno não deve ter nada além da pergunta
        """

        completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": prompt
                }
            ],
            model="llama3-70b-8192"
        )

        return completion.choices[0].message.content

    def analyze_response(self, question: str, answer: str) -> Assessment:
        prompt = f"""
        Analise a resposta dada para a pergunta abaixo:

        Pergunta: {question}
        Resposta: {answer}

        Sua tarefa é:
        1. Avaliar a resposta comparando com a resposta ideal.
        2. Fornecer um feedback detalhado, apontando os acertos, erros e sugestões de melhoria.
        3. Atribuir um score em percentual (0% a 100%) que indique o quão correta a resposta está.

        Por favor, retorne a análise no seguinte formato:
        {{
            "score": "XX%",
            "feedback": "Seu feedback detalhado aqui..."
        }}
        """

        completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": prompt
                }
            ],
            model="llama3-70b-8192"
        )

        response_content = completion.choices[0].message.content
        result = json.loads(response_content, strict=False)
        score = result.get("score")
        feedback = result.get("feedback")
        return Assessment(feedback=feedback, score=score)
