#!/bin/bash
# Script para configurar Ollama com modelo Mistral

echo "🚀 Configurando Ollama com Mistral..."

# 1. Iniciar Ollama
echo "📦 Iniciando serviços Ollama..."
docker-compose -f docker-compose.ollama.yml up -d ollama

# Aguardar Ollama inicializar
echo "⏳ Aguardando Ollama inicializar..."
sleep 10

# 2. Verificar se Ollama está rodando
echo "🔍 Verificando status do Ollama..."
curl -s http://localhost:11434/api/tags || echo "❌ Ollama não está respondendo"

# 3. Fazer pull do modelo Mistral
echo "📥 Baixando modelo Mistral (pode demorar)..."
curl -X POST http://localhost:11434/api/pull -H "Content-Type: application/json" -d '{"name": "mistral"}'

# 4. Verificar modelos disponíveis
echo "📋 Modelos instalados:"
curl -s http://localhost:11434/api/tags | jq '.'

# 5. Iniciar servidor API
echo "🔥 Iniciando servidor API..."
docker-compose -f docker-compose.ollama.yml up -d llm-api

# 6. Iniciar N8N
echo "🎯 Iniciando N8N..."
docker-compose -f docker-compose.ollama.yml up -d n8n

echo "✅ Setup completo!"
echo "🌐 Ollama: http://localhost:11434"
echo "🤖 API: http://localhost:5000"
echo "⚡ N8N: http://localhost:5678 (admin/password123)"

# 7. Testar API
echo "🧪 Testando API..."
sleep 5
curl -X POST http://localhost:5000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral",
    "messages": [
      {"role": "user", "content": "Olá! Como você está?"}
    ],
    "temperature": 0.7,
    "max_tokens": 100
  }' | jq '.'
