# 🚀 Quick Start - Sistema de Chat AI

## Inicialização Rápida

### Opção 1: Script Automático
```powershell
.\setup_ollama.ps1
```

### Opção 2: Manual
```powershell
# 1. Iniciar todos os serviços
docker-compose -f docker-compose.ollama.yml up -d

# 2. Verificar se modelo existe (se não, será baixado automaticamente)
python setup_model.py

# 3. Testar sistema
python test_api.py
```

## 🌐 URLs dos Serviços

- **Ollama**: http://localhost:11434
- **API Chat**: http://localhost:5000
- **N8N**: http://localhost:5678 (admin/password123)

## 🔧 Comandos Úteis

```powershell
# Ver status dos containers
docker-compose -f docker-compose.ollama.yml ps

# Ver logs em tempo real
docker-compose -f docker-compose.ollama.yml logs -f llm-api

# Parar todos os serviços
docker-compose -f docker-compose.ollama.yml down

# Limpeza do sistema
.\cleanup.ps1
```

## 🧪 Teste Rápido via PowerShell

```powershell
$body = @{
    model = "mistral"
    messages = @(@{
        role = "user"
        content = "Olá! Me explique brevemente o que é IA."
    })
    temperature = 0.7
    max_tokens = 100
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:5000/v1/chat/completions" -Method Post -Body $body -ContentType "application/json"
```
