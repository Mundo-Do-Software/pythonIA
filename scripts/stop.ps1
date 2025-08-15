# =============================================================================
# SCRIPT DE PARADA - LLM API Stack
# =============================================================================

Write-Host "🛑 Parando LLM API Stack..." -ForegroundColor Red

# Parar serviços
docker-compose down

Write-Host "📊 Limpando recursos..." -ForegroundColor Yellow

# Mostrar status
docker-compose ps

Write-Host "✅ Stack parada com sucesso!" -ForegroundColor Green
