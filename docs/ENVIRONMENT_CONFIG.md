# Configuração de Variáveis de Ambiente

## 📋 Arquivo `.env`

O arquivo `config/.env` contém todas as configurações do sistema:

### 🔑 API Configuration
```env
API_KEY=dfdjhasdfgldfugydlsuiflhgd  # Chave de autenticação da API
API_HOST=0.0.0.0                   # Host da API (0.0.0.0 para todos)
API_PORT=5000                      # Porta da API
```

### 🤖 Ollama Configuration
```env
OLLAMA_HOST=0.0.0.0               # Host do Ollama
OLLAMA_PORT=11434                 # Porta do Ollama
OLLAMA_GPU_LAYERS=999             # Usar todas as camadas na GPU
OLLAMA_NUM_PARALLEL=2             # Processos paralelos
OLLAMA_MAX_LOADED_MODELS=1        # Máximo de modelos carregados
OLLAMA_FLASH_ATTENTION=1          # Flash Attention para RTX
OLLAMA_CONTEXT_LENGTH=2048        # Tamanho do contexto
OLLAMA_MAX_QUEUE=256              # Tamanho da fila
```

### 🗄️ Redis Configuration
```env
REDIS_HOST=redis                  # Host do Redis
REDIS_PORT=6379                   # Porta do Redis
REDIS_URL=redis://redis:6379      # URL completa do Redis
REDIS_MAX_MEMORY=512mb            # Memória máxima
REDIS_EVICTION_POLICY=allkeys-lru # Política de remoção
```

### 🔄 N8N Configuration
```env
N8N_HOST=0.0.0.0                  # Host do N8N
N8N_PORT=5678                     # Porta do N8N
N8N_PROTOCOL=http                 # Protocolo (http/https)
N8N_BASIC_AUTH_ACTIVE=true        # Ativar autenticação básica
N8N_BASIC_AUTH_USER=admin         # Usuário de login
N8N_BASIC_AUTH_PASSWORD=password123 # Senha de login
N8N_WEBHOOK_URL=http://localhost:5678 # URL dos webhooks
```

### 🐳 Docker Configuration
```env
NETWORK_NAME=llm-network          # Nome da rede Docker
CUDA_VISIBLE_DEVICES=0            # GPU específica
```

## 🎯 Nomes Padronizados dos Containers

| Serviço | Container Name | Descrição |
|---------|---------------|-----------|
| Ollama  | `llm-ollama`  | Backend LLM |
| API     | `llm-api`     | Servidor API Principal |
| Redis   | `llm-redis`   | Cache Database |
| N8N     | `llm-n8n`     | Workflow Automation |

## 🔧 Personalização

Para alterar configurações:

1. **Edite** `config/.env`
2. **Reconstrua** os containers:
   ```powershell
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

## 📊 Volumes Nomeados

- `llm-ollama-data`: Dados do Ollama
- `llm-redis-data`: Dados persistentes do Redis

## 🌐 Rede

Todos os serviços estão na rede `llm-network` para comunicação interna segura.
