# Imagem base oficial do Python (versão leve)
FROM python:3.11-slim

# Evita que o Python grave arquivos pyc e bufferize stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define diretório de trabalho no container
WORKDIR /app

# Instala dependências do sistema necessárias para compilar pacotes Python e cliente Postgres
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código (será sobrescrito pelo volume em dev, mas útil para prod)
COPY . .

# Comando padrão (pode ser sobrescrito pelo docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]