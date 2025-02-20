import json
import logging
import os

from dotenv import load_dotenv
from groq import Groq

from models import Assessment

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura o logger para o módulo atual
logger = logging.getLogger(__name__)


class GroqService:
    """
    Serviço para interagir com a API Groq.
    """

    def __init__(self):
        """
        Inicializa o serviço Groq, carregando a chave da API das variáveis de ambiente.
        Lança um erro se a chave da API não estiver configurada.
        """
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.error("GROQ_API_KEY não configurada nas variáveis de ambiente.")
            raise ValueError("GROQ_API_KEY não definida.")
        self.client = Groq(api_key=api_key)
        logger.info("GroqService inicializado com sucesso.")

    def create_question(self, theme: str):
        """
        Cria uma pergunta baseada no tema fornecido.

        Args:
            theme (str): O tema para o qual a pergunta será criada.

        Returns:
            str: A pergunta gerada.

        Raises:
            Exception: Se ocorrer um erro ao gerar a pergunta.
        """
        logger.info("Iniciando criação de pergunta para o tema: '%s'", theme)
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

        try:
            completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    }
                ],
                model="llama3-70b-8192"
            )
            question_text = completion.choices[0].message.content
            logger.info("Pergunta gerada com sucesso para o tema: '%s'", theme)
            return question_text
        except Exception as e:
            logger.error("Erro ao criar pergunta para o tema '%s': %s", theme, str(e), exc_info=True)
            raise Exception("Erro interno ao gerar a pergunta.")

    def analyze_response(self, question: str, answer: str) -> Assessment:
        """
        Analisa a resposta fornecida para uma pergunta específica.

        Args:
            question (str): A pergunta para a qual a resposta será analisada.
            answer (str): A resposta que será analisada.

        Returns:
            Assessment: Um objeto contendo o feedback e o score da análise.

        Raises:
            Exception: Se ocorrer um erro ao analisar a resposta.
            ValueError: Se a resposta recebida não estiver em formato JSON válido.
        """
        logger.info("Iniciando análise de resposta para a pergunta: '%.50s...'", question)
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

        try:
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
            logger.info("Resposta recebida com sucesso (primeiros 100 caracteres): %.100s", response_content)
        except Exception as e:
            logger.error("Erro ao analisar resposta para a pergunta '%.50s...': %s", question, str(e), exc_info=True)
            raise Exception("Erro interno ao analisar a resposta.")

        try:
            result = json.loads(response_content, strict=False)
        except Exception as e:
            logger.error("Erro ao interpretar resposta JSON: %s", str(e), exc_info=True)
            raise ValueError("Resposta em formato inválido.")

        score = result.get("score")
        feedback = result.get("feedback")
        logger.info("Análise concluída com sucesso, score: %s", score)
        return Assessment(feedback=feedback, score=score)
