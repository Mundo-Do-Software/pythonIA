FROM python:3.10-slim

# Argumentos de build
ARG API_PORT=5000

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório da aplicação
WORKDIR /app

# Instalar dependências Python básicas
RUN pip3 install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    pydantic==2.5.0 \
    requests \
    aiohttp \
    redis[hiredis]>=4.5.0 \
    sentence-transformers>=2.2.0 \
    numpy>=1.21.0

# Copiar servidor
COPY src/simple_llm_server.py /app/

# Criar diretório para modelos
RUN mkdir -p /app/models

# Variáveis de ambiente
ENV API_HOST=0.0.0.0
ENV API_PORT=${API_PORT}

# Expor porta
EXPOSE ${API_PORT}

# Comando para iniciar o servidor
CMD ["python", "simple_llm_server.py"]
