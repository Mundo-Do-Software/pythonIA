# N8N + IAS - Sistema de Inteligência Artificial Multi-Modelo

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-green.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)

## 🏗️ Arquitetura do Projeto

Este projeto implementa um sistema completo de IA com **cache semântico**, suporte **multi-modelo** e integração com **N8N** para automação de workflows.

### 📋 Características Principais
- 🚀 **Cache Semântico Inteligente** - 874.8x speedup com Redis + embeddings
- 🤖 **Multi-LLM Support** - Ollama, Mistral, Llama3.2
- ⚡ **API FastAPI** - Endpoints compatíveis com OpenAI
- 🔄 **N8N Integration** - Automação completa de workflows
- 🐳 **Docker Compose** - Deploy simplificado
- 🧪 **Testing Suite** - Testes automatizados

```
N8N+IAS/
├── 📂 src/                     # Código fonte principal
│   ├── simple_llm_server.py    # Servidor principal da API
│   ├── debug_models.py         # Utilitários de debug
│   └── llama_cpp_server_temp.py # Servidor alternativo
│
├── 📂 config/                  # Configurações
│   ├── Dockerfile              # Container da API
│   └── .env                    # Variáveis de ambiente
│
├── 📂 tests/                   # Testes organizados
│   ├── unit/                   # Testes unitários
│   ├── integration/            # Testes de integração
│   └── performance/            # Testes de performance
│
├── 📂 scripts/                 # Scripts de automação
│   ├── start.ps1               # Iniciar stack completa
│   ├── stop.ps1                # Parar todos serviços
│   └── pull-model.ps1          # Baixar modelos Ollama
│
├── 📂 docs/                    # Documentação completa
│   ├── ENVIRONMENT_CONFIG.md   # Configuração de variáveis
│   ├── CLEANUP_SUMMARY.md      # Histórico de limpeza
│   └── README.md               # Documentação técnica
│
├── 📂 workflows/               # Workflows N8N (.json)
├── 📂 models/                  # Modelos LLM (*.gguf)
├── 📂 n8n_data/               # Dados persistentes N8N
├── 📂 loras/                  # Adaptadores LoRA
├── 📄 docker-compose.yml       # Orquestração principal
├── 📄 run_tests.py             # Sistema de testes
├── 📄 .gitignore               # Arquivos ignorados
└── 📄 .dockerignore            # Build context otimizado
```

## 🚀 Quick Start

### 1. Configuração Inicial
```powershell
# Clonar o repositório
git clone <repo-url>
cd N8N+IAS

# Baixar modelo Ollama
./scripts/pull-model.ps1

# Configurar variáveis (editar se necessário)
# As configurações estão em config/.env
```

### 2. Iniciar Serviços
```powershell
# Iniciar stack completa
./scripts/start.ps1

# Ou iniciar manualmente
docker-compose up -d

# Parar serviços
./scripts/stop.ps1
```

### 3. URLs de Acesso
- **LLM API**: http://localhost:5000
- **N8N**: http://localhost:5678 (admin/password123)  
- **Redis**: localhost:6379
- **Ollama**: http://localhost:11434

### 4. Verificar Sistema
```powershell
# Executar testes automatizados
python run_tests.py

# Testar categorias específicas
python run_tests.py quick    # Testes rápidos
python run_tests.py cache    # Cache semântico
python run_tests.py api      # API endpoints
python run_tests.py all      # Todos os testes

# Status dos containers
docker-compose ps
```

## 🧪 Sistema de Testes

O projeto inclui uma **suite completa de testes** organizados em categorias:

### Testes Essenciais (`run_tests.py`)
- ✅ **API Super Rápida** - Conectividade básica
- ✅ **Teste Rápido Original** - Chat completions
- ✅ **Correção Bug Timeout** - Validação do cache semântico

### Estrutura de Testes
```
tests/
├── unit/              # Testes unitários isolados
├── integration/       # Testes de integração entre serviços  
├── performance/       # Benchmarks e testes de carga
├── test_super_quick.py    # Teste básico de conectividade
├── test_quick.py          # Teste de chat completion
└── test_bug_fix_final.py  # Validação do cache semântico
```

### Como Executar
```powershell
# Todos os testes essenciais
python run_tests.py

# Execução por categoria
python run_tests.py quick     # Apenas conectividade
python run_tests.py cache     # Cache + Redis
python run_tests.py api       # API completa
python run_tests.py help      # Ver opções
```
- `test_basic_api.py` - Testes básicos da API
- `test_simple_api.py` - Testes de funcionalidades simples
- `test_models.py` - Testes de seleção de modelos

### Testes de Integração (`tests/integration/`)
- `test_system_complete.py` - Testes completos do sistema
- `test_final_cache.py` - Testes do cache semântico
- `test_api.py` - Testes de integração da API

### Testes de Performance (`tests/performance/`)
- `test_semantic_cache.py` - Performance do cache semântico
- `test_concurrency.py` - Testes de concorrência
- `test_velocidade.py` - Benchmarks de velocidade

## 📚 Funcionalidades Principais

### ✅ Cache Semântico Inteligente
- **874.8x speedup** para perguntas similares
- Cache baseado em embeddings com similaridade > 85%
- Validação automática de respostas (não cacheia erros/timeouts)
- TTL configurável (300s padrão)

### ✅ Multi-Modelo Automático
- **Seleção inteligente** baseada no contexto
- Suporte a Mistral 7B e Llama 3.2 3B
- Fallback automático em caso de falha
- Otimização por tipo de consulta

### ✅ Infraestrutura Robusta
- **Docker Compose** para orquestração
- **Redis** para cache persistente
- **GPU acceleration** com NVIDIA
- **Health checks** e monitoramento

### ✅ Integração N8N
- Workflows prontos para automação
- Conectores para sistemas externos
- Processamento em lote

## 🔧 Configuração

### Variáveis de Ambiente
```env
# API Configuration
API_KEY=dfdjhasdfgldfugydlsuiflhgd
REDIS_URL=redis://redis:6379

# Ollama Configuration
OLLAMA_HOST=0.0.0.0
OLLAMA_GPU_LAYERS=999
OLLAMA_NUM_PARALLEL=2
OLLAMA_MAX_LOADED_MODELS=1
```

### Modelos Suportados
- **Mistral 7B** - Para consultas complexas e técnicas
- **Llama 3.2 3B** - Para consultas simples e rápidas
- **Auto-seleção** baseada em palavras-chave e tamanho

## �️ Tecnologias Utilizadas

### Backend
- **Python 3.10+** - Linguagem principal
- **FastAPI** - Framework web assíncrono
- **Uvicorn** - Servidor ASGI de alta performance
- **Pydantic** - Validação de dados

### Cache & Database
- **Redis 7** - Cache semântico persistente
- **sentence-transformers** - Embeddings para similaridade
- **paraphrase-multilingual-MiniLM-L12-v2** - Modelo de embeddings

### LLM & AI
- **Ollama** - Runtime para modelos locais
- **Mistral 7B** - Modelo principal (4.4GB)
- **Llama 3.2 3B** - Modelo rápido (2.0GB)

### Infrastructure
- **Docker Compose** - Orquestração de containers
- **NVIDIA Docker** - Aceleração GPU
- **N8N** - Automação de workflows

### Monitoring & Testing
- **Sistema de testes personalizado** - Validação automatizada
- **Health checks** - Monitoramento de serviços
- **Logs estruturados** - Debug e troubleshooting

## 📊 Performance Benchmarks

| Métrica | Cache Hit | Cache Miss | Speedup |
|---------|-----------|------------|---------|
| **Tempo Resposta** | 0.12-0.26s | 99.74s | **874.8x** |
| **Throughput** | ~4 req/s | ~0.01 req/s | **400x** |
| **Uso Memória** | Baixo | Alto | **Otimizado** |
| **Uso GPU** | Mínimo | Intensivo | **Eficiente** |

## 🔧 Configuração Avançada

### Variáveis de Ambiente Principais
```env
# API Configuration
API_KEY=dfdjhasdfgldfugydlsuiflhgd    # Chave de autenticação
API_HOST=0.0.0.0                     # Host da API
API_PORT=5000                        # Porta da API

# Cache Configuration  
REDIS_URL=redis://redis:6379          # URL do Redis
REDIS_MAX_MEMORY=512mb               # Memória máxima
REDIS_EVICTION_POLICY=allkeys-lru    # Política de remoção

# GPU Configuration
OLLAMA_GPU_LAYERS=999                # Usar todas camadas GPU
CUDA_VISIBLE_DEVICES=0               # GPU específica
```

### Modelos Disponíveis
- **🚀 Mistral 7B** (`mistral:latest`) - 4.4GB
  - Melhor para: consultas complexas, análises técnicas
  - Tempo médio: 8-12s por resposta
  
- **⚡ Llama 3.2 3B** (`llama3.2:3b`) - 2.0GB  
  - Melhor para: consultas simples, respostas rápidas
  - Tempo médio: 4-6s por resposta

### Cache Semântico
- **Threshold de Similaridade**: 85%
- **TTL (Time To Live)**: 300 segundos
- **Modelo de Embeddings**: paraphrase-multilingual-MiniLM-L12-v2
- **Validação**: Não cacheia erros ou timeouts

## 🔗 Endpoints da API

### POST `/v1/chat/completions`
Endpoint principal compatível com OpenAI API
```json
{
  "model": "auto",
  "messages": [{"role": "user", "content": "Sua pergunta"}],
  "max_tokens": 100
}
```

### GET `/` 
Health check e informações do sistema
```json
{
  "status": "running",
  "backend": "connected", 
  "model": "mistral",
  "api_version": "1.0.0"
}
```

## 🐛 Troubleshooting

### Problemas Comuns

**❌ API não responde**
```powershell
# Verificar containers
docker-compose ps

# Ver logs
docker logs llm-api
docker logs llm-ollama

# Reiniciar serviços
docker-compose restart
```

**❌ Cache não funcionando**
```powershell
# Verificar Redis
docker logs llm-redis

# Testar conexão
python -c "import redis; r=redis.Redis(host='localhost', port=6379); print(r.ping())"
```

**❌ Modelo não encontrado**
```powershell
# Listar modelos
docker exec llm-ollama ollama list

# Baixar modelo
./scripts/pull-model.ps1
```

**❌ Testes falhando**
```powershell
# Verificar serviços primeiro
python run_tests.py

# Executar teste específico
python tests/test_super_quick.py
```

### Performance Issues

**🐌 Respostas lentas**
- Verificar se GPU está sendo usada: `nvidia-smi`
- Conferir configuração CUDA_VISIBLE_DEVICES
- Considerar usar modelo menor (Llama 3.2 3B)

**💾 Alto uso de memória**
- Ajustar REDIS_MAX_MEMORY no `.env`
- Reduzir OLLAMA_MAX_LOADED_MODELS para 1
- Limpar cache: `docker exec llm-redis redis-cli FLUSHALL`

## � Estrutura de Arquivos

### Arquivos Importantes
- `docker-compose.yml` - Orquestração principal
- `config/.env` - Variáveis de ambiente
- `config/Dockerfile` - Build da API
- `src/simple_llm_server.py` - Servidor principal
- `run_tests.py` - Sistema de testes
- `.gitignore` / `.dockerignore` - Arquivos ignorados

### Dados Persistentes
- `models/` - Modelos Ollama (montado como volume)
- `n8n_data/` - Dados N8N (workflows, configurações)
- `redis_data/` - Cache Redis (volume Docker)
- `ollama_data/` - Dados Ollama (volume Docker)

## 🤝 Contribuição

### Como Contribuir
1. **Fork** o repositório
2. **Crie** uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. **Commit** suas mudanças (`git commit -m 'Add: nova feature'`)
4. **Push** para a branch (`git push origin feature/nova-feature`)
5. **Abra** um Pull Request

### Desenvolvimento Local
```powershell
# Clone o projeto
git clone <repo-url>
cd N8N+IAS

# Configure ambiente
./scripts/pull-model.ps1

# Inicie desenvolvimento
docker-compose up -d

# Execute testes
python run_tests.py
```

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo `LICENSE` para mais detalhes.

## 🎯 Roadmap

- [ ] **API v2** - Endpoints estendidos
- [ ] **Multi-GPU** - Suporte a múltiplas GPUs  
- [ ] **Streaming** - Respostas em tempo real
- [ ] **RAG Integration** - Retrieval Augmented Generation
- [ ] **Web Interface** - Dashboard de monitoramento
- [ ] **Kubernetes** - Deploy em cluster

---

**Desenvolvido com ❤️ para comunidade de IA**
  "model": "auto",
  "messages": [
    {"role": "user", "content": "Sua pergunta aqui"}
  ],
  "temperature": 0.7,
  "max_tokens": 512
}
```

### GET `/v1/models`
```json
{
  "data": [
    {"id": "mistral", "object": "model"},
    {"id": "llama3.2:3b", "object": "model"}
  ]
}
```

## 📖 Documentação Detalhada

- [📋 Guia de Configuração](docs/guides/QUICKSTART.md)
- [🔧 Setup do Postman](docs/guides/POSTMAN_GUIDE.md)
- [🏗️ Arquitetura do Sistema](docs/architecture/SISTEMA_FINAL_FUNCIONANDO.md)
- [💰 Exemplos Financeiros](docs/examples/FINANCIAL_KPI_EXAMPLES.md)
- [🏍️ Caso de Uso - Motos](docs/examples/MODELO_RICARDO_MOTOS.md)

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Execute os testes: `python -m pytest tests/`
4. Commit: `git commit -m "Adiciona nova funcionalidade"`
5. Push: `git push origin feature/nova-funcionalidade`
6. Abra um Pull Request

## 🛠️ Troubleshooting

### Problemas Comuns

1. **API não responde**
   ```bash
   docker-compose -f docker-compose.ollama.yml logs llm-api
   ```

2. **Cache não funciona**
   ```bash
   docker exec redis-cache redis-cli ping
   ```

3. **Modelo não encontrado**
   ```bash
   docker exec ollama-server ollama list
   ```

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**Desenvolvido com ❤️ para automação inteligente de processos**