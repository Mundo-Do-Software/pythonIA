# Guia de Contribuição

Obrigado por considerar contribuir com o **N8N+IAS**! 🎉

## 🤝 Como Contribuir

### 1. Fork & Clone
```bash
# Fork o repositório no GitHub
# Clone seu fork
git clone https://github.com/SEU-USERNAME/N8N+IAS.git
cd N8N+IAS
```

### 2. Configurar Ambiente
```powershell
# Instalar Docker Desktop
# Baixar modelos
./scripts/pull-model.ps1

# Iniciar desenvolvimento
docker-compose up -d

# Verificar se tudo funciona
python run_tests.py
```

### 3. Criar Branch
```bash
git checkout -b feature/sua-nova-feature
# ou
git checkout -b fix/corrigir-bug
# ou  
git checkout -b docs/melhorar-documentacao
```

### 4. Desenvolver
- Siga as **convenções de código** existentes
- Adicione **testes** para novas funcionalidades
- **Documente** mudanças importantes
- **Teste** localmente antes de commit

### 5. Commit & Push
```bash
# Commits semânticos
git commit -m "feat: adicionar cache TTL configurável"
git commit -m "fix: corrigir timeout no Redis"
git commit -m "docs: atualizar README com novos endpoints"

git push origin feature/sua-nova-feature
```

### 6. Pull Request
- **Título claro** descrevendo a mudança
- **Descrição detalhada** do que foi alterado
- **Referenciar issues** relacionadas
- **Screenshots** se applicable

## 📋 Tipos de Contribuição

### 🐛 Bug Reports
**Use o template:**
```markdown
**Descrição do Bug**
Descrição clara do problema

**Passos para Reproduzir**
1. Faça isso...
2. Execute aquilo...
3. Veja o erro

**Comportamento Esperado**
O que deveria acontecer

**Comportamento Atual**
O que está acontecendo

**Ambiente**
- OS: Windows 11
- Python: 3.10
- Docker: 24.0.6

**Logs**
```
Logs relevantes aqui
```
```

### ✨ Feature Requests
**Estrutura sugerida:**
```markdown
**Problema/Necessidade**
Descreva o problema que a feature resolveria

**Solução Proposta**
Como você imagina que deveria funcionar

**Alternativas Consideradas**
Outras abordagens que você pensou

**Contexto Adicional**
Screenshots, exemplos, referências
```

### 📚 Melhorias na Documentação
- Corrigir typos e erros
- Adicionar exemplos práticos
- Melhorar explicações técnicas
- Traduzir para outros idiomas

### 🧪 Testes
- Adicionar novos casos de teste
- Melhorar cobertura de código
- Otimizar performance dos testes
- Corrigir testes instáveis

## 🎨 Padrões de Código

### Python
```python
# Use type hints
def process_query(query: str, model: str = "auto") -> dict:
    """Process user query with specified model."""
    pass

# Docstrings claras
def cache_response(key: str, value: dict, ttl: int = 300) -> bool:
    """
    Cache response with TTL.
    
    Args:
        key: Cache key identifier
        value: Response data to cache
        ttl: Time to live in seconds
        
    Returns:
        True if cached successfully
    """
    pass

# Error handling apropriado
try:
    result = ollama_client.generate(prompt)
except OllamaConnectionError as e:
    logger.error(f"Ollama connection failed: {e}")
    return {"error": "Service unavailable"}
```

### Docker
```dockerfile
# Comentários claros
FROM python:3.10-slim

# Múltiplas instruções em uma linha
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Variáveis de ambiente bem definidas
ENV API_HOST=0.0.0.0
ENV API_PORT=5000
```

### Commits Semânticos
```bash
feat: nova funcionalidade
fix: correção de bug  
docs: documentação
style: formatação, sem mudança de lógica
refactor: refatoração de código
test: adição ou correção de testes
chore: tarefas de build, config, etc
```

## 🧪 Testando Suas Mudanças

### Antes do Commit
```powershell
# Testes essenciais
python run_tests.py

# Testes específicos
python run_tests.py cache    # Cache semântico
python run_tests.py api      # API endpoints

# Build Docker (se alterou Dockerfile)
docker-compose build --no-cache
docker-compose up -d

# Verificar serviços
docker-compose ps
```

### Adicionando Novos Testes
```python
# tests/test_nova_feature.py
import requests

def test_nova_feature():
    """Test nova funcionalidade."""
    response = requests.post(
        "http://localhost:5000/nova-rota",
        json={"param": "valor"}
    )
    assert response.status_code == 200
    assert "expected" in response.json()
```

## 📝 Documentação

### README Updates
- Mantenha a estrutura existente
- Adicione exemplos práticos
- Atualize badges se necessário
- Teste todos os comandos documentados

### Código
- Docstrings para funções públicas
- Comentários para lógica complexa
- Type hints sempre que possível
- README específico para módulos

## 🏷️ Processo de Review

### O que Verificamos
- ✅ **Funcionalidade** - Faz o que promete?
- ✅ **Testes** - Tem cobertura adequada?
- ✅ **Documentação** - Está bem documentado?
- ✅ **Performance** - Não degrada o sistema?
- ✅ **Compatibilidade** - Funciona com versões atuais?

### Timeline
- **Review inicial**: 2-3 dias
- **Feedback**: Via comentários no PR
- **Merge**: Após aprovação de maintainer

## 🆘 Precisa de Ajuda?

### Recursos
- **README.md** - Documentação principal
- **docs/** - Documentação técnica detalhada
- **tests/** - Exemplos de como testar
- **Issues** - Perguntas e discussões

### Contato
- **GitHub Issues** - Para bugs e features
- **GitHub Discussions** - Para dúvidas gerais
- **Pull Requests** - Para contribuições de código

## 🎯 Prioridades Atuais

### High Priority
- 🐛 **Bug fixes** - Correções têm prioridade
- 📚 **Documentação** - Sempre bem-vinda
- 🧪 **Testes** - Melhorar cobertura

### Medium Priority  
- ✨ **Features** - Novas funcionalidades
- ⚡ **Performance** - Otimizações
- 🔧 **Refactoring** - Melhorias no código

### Future
- 🚀 **API v2** - Expansão da API
- 🌐 **Multi-language** - Suporte a outras linguagens
- ☸️ **Kubernetes** - Deploy em cluster

---

**Obrigado por contribuir! Sua ajuda faz a diferença! 🚀**
