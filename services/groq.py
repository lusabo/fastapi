import os

from dotenv import load_dotenv
from groq import Groq

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
