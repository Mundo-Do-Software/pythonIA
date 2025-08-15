# =============================================================================
# SCRIPT DE INICIALIZAÇÃO - LLM API + N8N + REDIS
# =============================================================================

Write-Host "🚀 Iniciando LLM API Stack..." -ForegroundColor Green

# Verificar se Docker está rodando
try {
    docker version | Out-Null
    Write-Host "✅ Docker está ativo" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker não está rodando. Inicie o Docker Desktop primeiro." -ForegroundColor Red
    exit 1
}

# Verificar se existe arquivo .env
if (!(Test-Path "config\.env")) {
    Write-Host "❌ Arquivo config\.env não encontrado!" -ForegroundColor Red
    exit 1
}

Write-Host "📋 Carregando variáveis de ambiente..." -ForegroundColor Yellow

# Verificar se existe modelo Ollama
if (!(Test-Path "models\*")) {
    Write-Host "⚠️  Pasta models está vazia. Execute 'scripts\pull-model.ps1' primeiro." -ForegroundColor Yellow
}

# Construir e iniciar serviços
Write-Host "🔨 Construindo containers..." -ForegroundColor Blue
docker-compose build --no-cache

Write-Host "🏃 Iniciando serviços..." -ForegroundColor Blue
docker-compose up -d

# Aguardar serviços
Write-Host "⏳ Aguardando serviços iniciarem..." -ForegroundColor Yellow
Start-Sleep 10

# Verificar status
Write-Host "`n📊 Status dos serviços:" -ForegroundColor Cyan
docker-compose ps

Write-Host "`n🎯 URLs de acesso:" -ForegroundColor Green
Write-Host "• LLM API: http://localhost:5000" -ForegroundColor White
Write-Host "• N8N: http://localhost:5678 (admin/password123)" -ForegroundColor White
Write-Host "• Redis: localhost:6379" -ForegroundColor White
Write-Host "• Ollama: http://localhost:11434" -ForegroundColor White

Write-Host "`n✅ Stack iniciada com sucesso!" -ForegroundColor Green
