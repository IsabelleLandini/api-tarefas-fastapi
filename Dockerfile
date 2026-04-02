# Usa uma imagem leve do Python
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala o Poetry
RUN  pip install poetry

# Copia os arquivos de configuração do Poetry
COPY  pyproject.toml poetry.lock* /app/

# Configura o Poetry para não criar ambientes virtuais dentro do container
# e instala as dependências
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# Copia o restante do código da aplicação
COPY . /app/

# Expõe a porta que o FastAPI usa
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
