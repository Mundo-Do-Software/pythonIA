# Script para inicializar modelos DeepSeek no GCP
param(
    [string]$ProjectId,
    [string]$Zone = "us-central1-a",
    [string]$ClusterName = "llm-deepseek-cluster"
)

if (-not $ProjectId) {
    # Tentar ler do arquivo de configuração
    if (Test-Path "gcp\.gcp-config.json") {
        $config = Get-Content "gcp\.gcp-config.json" | ConvertFrom-Json
        $ProjectId = $config.project_id
        $Zone = $config.zone
    } else {
        Write-Host "❌ ProjectId é obrigatório. Use: .\init-deepseek.ps1 -ProjectId SEU-PROJETO" -ForegroundColor Red
        exit 1
    }
}

Write-Host "🧠 Inicializando modelos DeepSeek no GCP..." -ForegroundColor Green
Write-Host "📋 Projeto: $ProjectId" -ForegroundColor Cyan
Write-Host "🌎 Zone: $Zone" -ForegroundColor Cyan

# 1. Configurar kubectl
Write-Host "🔧 Configurando kubectl..." -ForegroundColor Yellow
gcloud container clusters get-credentials $ClusterName --zone=$Zone --project=$ProjectId

# 2. Verificar se Ollama está rodando
Write-Host "🔍 Verificando status do Ollama..." -ForegroundColor Yellow
try {
    $ollama_status = kubectl get pods -l app=ollama -o jsonpath='{.items[0].status.phase}' 2>$null
    if ($ollama_status -eq "Running") {
        Write-Host "✅ Ollama está rodando!" -ForegroundColor Green
    } else {
        Write-Host "❌ Ollama não está rodando. Status: $ollama_status" -ForegroundColor Red
        Write-Host "🔄 Aguardando Ollama ficar pronto..." -ForegroundColor Yellow
        kubectl wait --for=condition=ready pod -l app=ollama --timeout=300s
    }
} catch {
    Write-Host "❌ Erro ao verificar status do Ollama" -ForegroundColor Red
    exit 1
}

# 3. Obter nome do pod Ollama
$ollama_pod = kubectl get pods -l app=ollama -o jsonpath='{.items[0].metadata.name}' 2>$null
if (-not $ollama_pod) {
    Write-Host "❌ Pod Ollama não encontrado" -ForegroundColor Red
    exit 1
}

Write-Host "🎯 Pod Ollama encontrado: $ollama_pod" -ForegroundColor Cyan

# 4. Verificar modelos já instalados
Write-Host "📋 Verificando modelos já instalados..." -ForegroundColor Yellow
try {
    $existing_models = kubectl exec $ollama_pod -- ollama list 2>$null
    Write-Host "Modelos existentes:" -ForegroundColor Cyan
    Write-Host $existing_models -ForegroundColor DarkCyan
} catch {
    Write-Host "⚠️ Não foi possível listar modelos existentes" -ForegroundColor Yellow
}

# 5. Instalar DeepSeek 1.3B (modelo rápido)
Write-Host "📥 Instalando DeepSeek 1.3B (modelo rápido)..." -ForegroundColor Yellow
try {
    kubectl exec $ollama_pod -- ollama pull deepseek-coder:1.3b
    Write-Host "✅ DeepSeek 1.3B instalado com sucesso!" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao instalar DeepSeek 1.3B" -ForegroundColor Red
}

# 6. Instalar DeepSeek 6.7B (modelo completo)
Write-Host "📥 Instalando DeepSeek 6.7B (modelo completo - pode demorar até 30 min)..." -ForegroundColor Yellow
Write-Host "⏳ Este é um modelo grande, seja paciente..." -ForegroundColor Magenta

try {
    kubectl exec $ollama_pod -- ollama pull deepseek-coder:6.7b
    Write-Host "✅ DeepSeek 6.7B instalado com sucesso!" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao instalar DeepSeek 6.7B" -ForegroundColor Red
    Write-Host "⚠️ Continuando com apenas o modelo 1.3B..." -ForegroundColor Yellow
}

# 7. Verificar instalação final
Write-Host "🔍 Verificando instalação final..." -ForegroundColor Yellow
try {
    $final_models = kubectl exec $ollama_pod -- ollama list
    Write-Host "✅ Modelos instalados:" -ForegroundColor Green
    Write-Host $final_models -ForegroundColor Cyan
} catch {
    Write-Host "❌ Erro ao verificar modelos finais" -ForegroundColor Red
}

# 8. Testar modelos
Write-Host "🧪 Testando modelo DeepSeek 1.3B..." -ForegroundColor Yellow
try {
    $test_response = kubectl exec $ollama_pod -- ollama run deepseek-coder:1.3b "Hello, respond with just 'DeepSeek 1.3B working'"
    if ($test_response -like "*DeepSeek*") {
        Write-Host "✅ DeepSeek 1.3B funcionando!" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Resposta inesperada do DeepSeek 1.3B" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Erro ao testar DeepSeek 1.3B" -ForegroundColor Red
}

# 9. Obter informações do serviço para teste da API
Write-Host "🌐 Obtendo informações do serviço..." -ForegroundColor Yellow
try {
    $ollama_service_ip = kubectl get service ollama-service -o jsonpath='{.spec.clusterIP}'
    Write-Host "🔗 Ollama Service IP: $ollama_service_ip:11434" -ForegroundColor Cyan
    
    # Teste interno do serviço
    Write-Host "🧪 Testando conectividade interna..." -ForegroundColor Yellow
    kubectl exec $ollama_pod -- curl -s "http://ollama-service:11434/api/tags" | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Serviço Ollama acessível internamente" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Problema de conectividade interna" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ Não foi possível obter informações do serviço" -ForegroundColor Yellow
}

# 10. Informações finais
Write-Host ""
Write-Host "✅ Inicialização dos modelos DeepSeek concluída!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Resumo dos modelos:" -ForegroundColor Yellow
Write-Host "   🚀 deepseek-coder:1.3b - Para respostas rápidas" -ForegroundColor Cyan
Write-Host "   🧠 deepseek-coder:6.7b - Para análises complexas" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔧 Comandos úteis:" -ForegroundColor Yellow
Write-Host "   Ver pods: kubectl get pods -l app=ollama" -ForegroundColor White
Write-Host "   Ver logs: kubectl logs $ollama_pod -f" -ForegroundColor White
Write-Host "   Executar comando: kubectl exec $ollama_pod -- ollama list" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Próximo passo: Teste a API em https://$ProjectId.appspot.com/" -ForegroundColor Magenta
