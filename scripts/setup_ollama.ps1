# Script PowerShell para configurar Ollama com DeepSeek
Write-Host "🚀 Configurando Ollama com modelos DeepSeek..." -ForegroundColor Green

# 1. Iniciar Ollama
Write-Host "📦 Iniciando serviços Ollama..." -ForegroundColor Yellow
docker-compose up -d ollama

# Aguardar Ollama inicializar
Write-Host "⏳ Aguardando Ollama inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 20

# 2. Verificar se Ollama está rodando
Write-Host "🔍 Verificando status do Ollama..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get
    Write-Host "✅ Ollama está rodando!" -ForegroundColor Green
} catch {
    Write-Host "❌ Ollama não está respondendo" -ForegroundColor Red
    Write-Host "🔄 Tentando aguardar mais 15 segundos..." -ForegroundColor Yellow
    Start-Sleep -Seconds 15
}

# 3. Fazer pull dos modelos DeepSeek
Write-Host "📥 Baixando DeepSeek 1.3B (modelo rápido)..." -ForegroundColor Yellow
$pullBody1 = @{
    name = "deepseek-coder:1.3b"
} | ConvertTo-Json

try {
    Invoke-RestMethod -Uri "http://localhost:11434/api/pull" -Method Post -Body $pullBody1 -ContentType "application/json" -TimeoutSec 1800
    Write-Host "✅ DeepSeek 1.3B baixado com sucesso!" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao baixar DeepSeek 1.3B: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "📥 Baixando DeepSeek 6.7B (modelo completo - pode demorar até 30 min)..." -ForegroundColor Yellow
$pullBody2 = @{
    name = "deepseek-coder:6.7b"
} | ConvertTo-Json

try {
    Invoke-RestMethod -Uri "http://localhost:11434/api/pull" -Method Post -Body $pullBody2 -ContentType "application/json" -TimeoutSec 3600
    Write-Host "✅ DeepSeek 6.7B baixado com sucesso!" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao baixar DeepSeek 6.7B: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "⚠️ Continuando com apenas o modelo 1.3B..." -ForegroundColor Yellow
}

# 4. Verificar modelos disponíveis
Write-Host "📋 Verificando modelos instalados..." -ForegroundColor Yellow
try {
    $models = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get
    $models.models | ForEach-Object { Write-Host "   - $($_.name)" -ForegroundColor Cyan }
} catch {
    Write-Host "❌ Erro ao listar modelos" -ForegroundColor Red
}

# 5. Iniciar Redis primeiro
Write-Host "🔴 Iniciando Redis..." -ForegroundColor Yellow
docker-compose up -d redis
Start-Sleep -Seconds 5

# 6. Iniciar servidor API
Write-Host "🔥 Iniciando servidor API..." -ForegroundColor Yellow
docker-compose up -d llm-api

# 7. Iniciar N8N
Write-Host "🎯 Iniciando N8N..." -ForegroundColor Yellow
docker-compose up -d n8n

Write-Host "✅ Setup completo!" -ForegroundColor Green
Write-Host "🌐 Ollama: http://localhost:11434" -ForegroundColor Cyan
Write-Host "🤖 API: http://localhost:5000" -ForegroundColor Cyan
Write-Host "⚡ N8N: http://localhost:5678 (admin/password123)" -ForegroundColor Cyan

# 8. Testar API com DeepSeek
Write-Host "🧪 Testando API em 15 segundos..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

$testBody = @{
    model = "auto"
    messages = @(
        @{
            role = "user"
            content = "Olá! Explique brevemente como funciona o modelo DeepSeek."
        }
    )
    temperature = 0.7
    max_tokens = 150
} | ConvertTo-Json -Depth 3

try {
    $testResponse = Invoke-RestMethod -Uri "http://localhost:5000/v1/chat/completions" -Method Post -Body $testBody -ContentType "application/json"
    Write-Host "✅ Teste da API bem-sucedido!" -ForegroundColor Green
    Write-Host "📝 Resposta: $($testResponse.choices[0].message.content)" -ForegroundColor White
    
    if ($testResponse.backend) {
        Write-Host "🧠 Backend usado: $($testResponse.backend)" -ForegroundColor Magenta
    }
} catch {
    Write-Host "❌ Erro no teste da API: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "🔄 Tentando teste básico..." -ForegroundColor Yellow
    
    # Teste de fallback mais simples
    try {
        $fallbackTest = Invoke-RestMethod -Uri "http://localhost:5000/" -Method Get
        Write-Host "✅ API está respondendo: $($fallbackTest.status)" -ForegroundColor Green
    } catch {
        Write-Host "❌ API não está respondendo" -ForegroundColor Red
    }
}

Write-Host "🎉 Configuração finalizada! Seus serviços estão rodando." -ForegroundColor Green
