FROM python:3.12-slim

# Instala dependências do sistema necessárias para o PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN pip install poetry

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências primeiro (cache eficiente)
COPY pyproject.toml poetry.lock ./

# Instala as dependências sem criar virtualenv (desnecessário no container)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copia o restante do projeto
COPY . .

# Expõe a porta da aplicação
EXPOSE 8000

# Comando padrão
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]