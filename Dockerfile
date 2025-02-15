# Usando a imagem do Python slim
FROM python:3.10-slim
# Define o diretório de trabalho
WORKDIR /app
# Copia os requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copia o resto do código para o diretório de trabalho
COPY . .
# Expõe a porta 8000 para acesso externo
EXPOSE 8000
# Comando para iniciar a aplicação
CMD ["fastapi", "run", "main.py"]