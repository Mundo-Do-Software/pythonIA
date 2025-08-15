# Script para limpar logs e dados temporários
Write-Host "🧹 Limpando arquivos temporários..." -ForegroundColor Yellow

# Limpar logs do N8N antigos
if (Test-Path "n8n_data\n8nEventLog-*.log") {
    Write-Host "📝 Removendo logs antigos do N8N..." -ForegroundColor Cyan
    Remove-Item -Path "n8n_data\n8nEventLog-*.log" -Force
}

# Limpar cache do Docker (opcional)
Write-Host "🐳 Limpando cache do Docker..." -ForegroundColor Cyan
docker system prune -f

# Limpar imagens Docker não utilizadas
Write-Host "🗑️ Removendo imagens Docker órfãs..." -ForegroundColor Cyan
docker image prune -f

Write-Host "✅ Limpeza concluída!" -ForegroundColor Green
