# =============================================================================
# SCRIPT DE FINE-TUNING AUTOMÁTICO
# =============================================================================

Write-Host "🧠 Iniciando Fine-Tuning Automático..." -ForegroundColor Green

# Verificar se os serviços estão rodando
Write-Host "📋 Verificando serviços..." -ForegroundColor Yellow

try {   
    Invoke-RestMethod -Uri "http://localhost:5000/" -TimeoutSec 5 | Out-Null
    Write-Host "✅ API está rodando" -ForegroundColor Green
} catch {
    Write-Host "❌ API não está acessível. Execute 'docker-compose up -d' primeiro." -ForegroundColor Red
    exit 1
}

try {
    $redisTest = docker exec llm-redis redis-cli ping
    if ($redisTest -eq "PONG") {
        Write-Host "✅ Redis está rodando" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Redis não está acessível." -ForegroundColor Red
    exit 1
}

# Verificar dados disponíveis
Write-Host "📊 Analisando dados de cache..." -ForegroundColor Blue

$cacheKeys = docker exec llm-redis redis-cli --raw KEYS "cache:*" | Measure-Object | Select-Object -ExpandProperty Count
Write-Host "🔍 Encontradas $cacheKeys entradas no cache" -ForegroundColor Cyan

if ($cacheKeys -lt 10) {
    Write-Host "⚠️  Poucos dados disponíveis para fine-tuning ($cacheKeys entradas)" -ForegroundColor Yellow
    Write-Host "   Execute algumas consultas na API primeiro para gerar dados de treinamento." -ForegroundColor Yellow
    
    $continue = Read-Host "Continuar mesmo assim? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        Write-Host "Fine-tuning cancelado." -ForegroundColor Yellow
        exit 0
    }
}

# Executar fine-tuning
Write-Host "🚀 Executando fine-tuning automático..." -ForegroundColor Blue
Write-Host "   Isso pode demorar alguns minutos..." -ForegroundColor Gray

try {
    python src/fine_tuning/auto_fine_tune.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Fine-tuning concluído com sucesso!" -ForegroundColor Green
        
        # Listar adaptadores LoRA criados
        if (Test-Path "loras/domain_specific") {
            $adapters = Get-ChildItem "loras/domain_specific" -Filter "*.safetensors" | Measure-Object | Select-Object -ExpandProperty Count
            Write-Host "🎯 Adaptadores LoRA criados: $adapters" -ForegroundColor Green
        }
        
        # Mostrar relatório se existir
        $latestReport = Get-ChildItem "training_data" -Filter "training_report_*.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if ($latestReport) {
            Write-Host "📋 Relatório disponível: $($latestReport.Name)" -ForegroundColor Cyan
            
            $report = Get-Content $latestReport.FullName | ConvertFrom-Json
            Write-Host "📊 Estatísticas:" -ForegroundColor White
            Write-Host "   • Total de conversas: $($report.total_conversations)" -ForegroundColor White
            Write-Host "   • Adaptadores treinados: $($report.trained_adapters.Count)" -ForegroundColor White
            
            foreach ($adapter in $report.trained_adapters) {
                Write-Host "   • $($adapter.domain): $($adapter.examples_count) exemplos" -ForegroundColor White
            }
        }
        
    } else {
        Write-Host "❌ Erro durante o fine-tuning" -ForegroundColor Red
        exit 1
    }
    
} catch {
    Write-Host "❌ Erro ao executar fine-tuning: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`n🎉 Processo concluído!" -ForegroundColor Green
Write-Host "📚 Para usar os adaptadores, eles precisam ser carregados no Ollama" -ForegroundColor Yellow
Write-Host "📖 Consulte a documentação para detalhes de implementação" -ForegroundColor Yellow
