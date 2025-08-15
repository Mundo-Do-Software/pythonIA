# Guia de Testes

## 🧪 Estrutura de Testes

### 📁 Testes Unitários (`tests/unit/`)
Testes focados em componentes individuais:

- **test_basic_api.py** - Testes básicos da API REST
- **test_simple_api.py** - Funcionalidades simples
- **test_models.py** - Seleção automática de modelos
- **test_auto_selection.py** - Algoritmo de seleção
- **test_debug_validation.py** - Validação de respostas

### 📁 Testes de Integração (`tests/integration/`)
Testes de componentes integrados:

- **test_system_complete.py** - Sistema completo end-to-end
- **test_final_cache.py** - Cache semântico integrado
- **test_api.py** - Integração API + Ollama
- **test_financial_complete.py** - Casos financeiros completos
- **test_debug_complete.py** - Debug de integração

### 📁 Testes de Performance (`tests/performance/`)
Benchmarks e otimizações:

- **test_semantic_cache.py** - Performance do cache semântico
- **test_performance_comparison.py** - Comparações de velocidade
- **test_concurrency.py** - Testes de concorrência
- **test_velocidade.py** - Benchmarks de velocidade
- **test_redis_cache.py** - Performance do Redis

## 🚀 Executando Testes

### Testes Rápidos (Unitários)
```bash
# API básica
python tests/unit/test_basic_api.py

# Seleção de modelos
python tests/unit/test_models.py
```

### Testes Completos (Integração)
```bash
# Sistema completo
python tests/integration/test_system_complete.py

# Cache semântico
python tests/integration/test_final_cache.py
```

### Benchmarks (Performance)
```bash
# Cache semântico (874.8x speedup)
python tests/performance/test_semantic_cache.py

# Comparação de velocidade
python tests/performance/test_performance_comparison.py
```

## 📊 Resultados Esperados

### Cache Semântico
- **Cache Hit**: 0.12-0.26s
- **Cache Miss**: 99.74s  
- **Speedup**: 874.8x
- **Similaridade**: > 85%

### API Response
- **Resposta Simples**: < 2s
- **Resposta Complexa**: 30-60s
- **Timeout**: 120s
- **Availability**: > 99%

## 🔧 Configuração de Testes

### Pré-requisitos
```bash
# Instalar dependências
pip install requests redis

# Verificar serviços
docker-compose -f docker-compose.ollama.yml ps
```

### Variáveis de Ambiente
```env
API_URL=http://localhost:5000
API_KEY=dfdjhasdfgldfugydlsuiflhgd
REDIS_HOST=localhost
REDIS_PORT=6379
```

## 🎯 Casos de Teste Específicos

### Financeiro
- **test_financial_kpi.py** - KPIs financeiros
- **test_financial_simple.py** - Consultas básicas

### Motocicletas (Ricardo)
- **test_motocicletas.py** - Sistema de diagnóstico
- **test_moto_diagnostico.py** - Diagnósticos avançados
- **test_moto_simples.py** - Consultas básicas

### Especialistas
- **test_specialists.py** - Sistema multi-especialista

## 🔍 Debug e Troubleshooting

### Logs de Teste
```bash
# API logs
docker logs simple-llm-api --tail 50

# Redis logs  
docker logs redis-cache --tail 20

# Ollama logs
docker logs ollama-server --tail 30
```

### Limpeza de Cache
```bash
# Limpar Redis
docker exec redis-cache redis-cli FLUSHALL

# Verificar chaves
docker exec redis-cache redis-cli KEYS "*"
```

## ✅ Checklist de Validação

- [ ] API responde em `/v1/chat/completions`
- [ ] Cache semântico funciona (speedup > 100x)
- [ ] Validação rejeita erros/timeouts
- [ ] Seleção automática de modelos
- [ ] Redis conectado e funcionando
- [ ] Ollama com modelos carregados
- [ ] Embeddings carregados corretamente

---

**Execute os testes regularmente para garantir qualidade!** 🚀
