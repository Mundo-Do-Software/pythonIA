# =============================================================================
# SCRIPT PARA BAIXAR MODELO OLLAMA
# =============================================================================

Write-Host "📥 Baixando modelo Ollama..." -ForegroundColor Green

# Modelo padrão
$MODEL = "mistral:7b-instruct"

Write-Host "🔍 Modelo selecionado: $MODEL" -ForegroundColor Yellow

# Verificar se Ollama está instalado
try {
    ollama version | Out-Null
    Write-Host "✅ Ollama encontrado" -ForegroundColor Green
} catch {
    Write-Host "❌ Ollama não está instalado. Baixe em: https://ollama.ai" -ForegroundColor Red
    exit 1
}

# Baixar modelo
Write-Host "⬇️  Baixando modelo (pode demorar alguns minutos)..." -ForegroundColor Blue
ollama pull $MODEL

# Verificar se download foi bem-sucedido
Write-Host "✅ Modelo $MODEL baixado com sucesso!" -ForegroundColor Green

# Listar modelos disponíveis
Write-Host "`n📋 Modelos disponíveis:" -ForegroundColor Cyan
ollama list
