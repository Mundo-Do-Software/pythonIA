# Script de testes para validar deployment no GCP
param(
    [string]$ProjectId,
    [string]$ApiUrl
)

if (-not $ProjectId) {
    if (Test-Path "gcp\.gcp-config.json") {
        $config = Get-Content "gcp\.gcp-config.json" | ConvertFrom-Json
        $ProjectId = $config.project_id
    } else {
        Write-Host "❌ ProjectId é obrigatório" -ForegroundColor Red
        exit 1
    }
}

if (-not $ApiUrl) {
    $ApiUrl = "https://$ProjectId.appspot.com"
}

Write-Host "🧪 Executando testes de validação do deployment..." -ForegroundColor Green
Write-Host "🌐 API URL: $ApiUrl" -ForegroundColor Cyan
Write-Host ""

# Função para fazer requisições HTTP
function Invoke-ApiTest {
    param(
        [string]$Url,
        [string]$Method = "GET",
        [hashtable]$Body = $null,
        [string]$Description
    )
    
    Write-Host "🔍 Testando: $Description" -ForegroundColor Yellow
    
    try {
        $params = @{
            Uri = $Url
            Method = $Method
            ContentType = "application/json"
            TimeoutSec = 30
        }
        
        if ($Body) {
            $params.Body = ($Body | ConvertTo-Json -Depth 3)
        }
        
        $response = Invoke-RestMethod @params
        Write-Host "   ✅ Sucesso" -ForegroundColor Green
        return $response
    } catch {
        Write-Host "   ❌ Falha: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# Testes
$results = @()

# 1. Teste de Health Check
Write-Host "1️⃣ TESTE: Health Check" -ForegroundColor Magenta
$health = Invoke-ApiTest -Url "$ApiUrl/" -Description "Health check básico"
if ($health) {
    Write-Host "   Status: $($health.status)" -ForegroundColor Cyan
    Write-Host "   Backend: $($health.backend)" -ForegroundColor Cyan
    $results += @{Test="Health Check"; Status="PASS"; Details="API está online"}
} else {
    $results += @{Test="Health Check"; Status="FAIL"; Details="API não está respondendo"}
}
Write-Host ""

# 2. Teste de Listagem de Modelos
Write-Host "2️⃣ TESTE: Listagem de Modelos" -ForegroundColor Magenta
$models = Invoke-ApiTest -Url "$ApiUrl/v1/models" -Description "Listar modelos disponíveis"
if ($models -and $models.data) {
    Write-Host "   Modelos encontrados: $($models.data.Count)" -ForegroundColor Cyan
    foreach ($model in $models.data) {
        Write-Host "   - $($model.id)" -ForegroundColor DarkCyan
    }
    $results += @{Test="List Models"; Status="PASS"; Details="$($models.data.Count) modelos encontrados"}
} else {
    $results += @{Test="List Models"; Status="FAIL"; Details="Não foi possível listar modelos"}
}
Write-Host ""

# 3. Teste de Chat com Modelo Rápido (1.3B)
Write-Host "3️⃣ TESTE: Chat com DeepSeek 1.3B (rápido)" -ForegroundColor Magenta
$chatBody1 = @{
    model = "auto"
    messages = @(
        @{
            role = "user"
            content = "Olá! Responda brevemente: você é o DeepSeek?"
        }
    )
    temperature = 0.7
    max_tokens = 50
}

$chat1 = Invoke-ApiTest -Url "$ApiUrl/v1/chat/completions" -Method "POST" -Body $chatBody1 -Description "Chat simples (deve usar 1.3B)"
if ($chat1 -and $chat1.choices) {
    $response1 = $chat1.choices[0].message.content
    Write-Host "   Resposta: $($response1.Substring(0, [Math]::Min(100, $response1.Length)))..." -ForegroundColor Cyan
    Write-Host "   Tokens: $($chat1.usage.total_tokens)" -ForegroundColor DarkCyan
    if ($chat1.backend) {
        Write-Host "   Backend: $($chat1.backend)" -ForegroundColor DarkCyan
    }
    $results += @{Test="Chat 1.3B"; Status="PASS"; Details="Resposta gerada com sucesso"}
} else {
    $results += @{Test="Chat 1.3B"; Status="FAIL"; Details="Falha na geração de resposta"}
}
Write-Host ""

# 4. Teste de Chat Complexo (deve usar 6.7B)
Write-Host "4️⃣ TESTE: Chat Complexo (deve usar 6.7B)" -ForegroundColor Magenta
$chatBody2 = @{
    model = "auto"
    messages = @(
        @{
            role = "user"
            content = "Explique detalhadamente como funciona a arquitetura de um sistema de machine learning em produção, incluindo aspectos de performance, escalabilidade e monitoramento."
        }
    )
    temperature = 0.7
    max_tokens = 300
}

$chat2 = Invoke-ApiTest -Url "$ApiUrl/v1/chat/completions" -Method "POST" -Body $chatBody2 -Description "Chat complexo (deve usar 6.7B)"
if ($chat2 -and $chat2.choices) {
    $response2 = $chat2.choices[0].message.content
    Write-Host "   Resposta: $($response2.Substring(0, [Math]::Min(150, $response2.Length)))..." -ForegroundColor Cyan
    Write-Host "   Tokens: $($chat2.usage.total_tokens)" -ForegroundColor DarkCyan
    if ($chat2.backend) {
        Write-Host "   Backend: $($chat2.backend)" -ForegroundColor DarkCyan
    }
    $results += @{Test="Chat 6.7B"; Status="PASS"; Details="Resposta complexa gerada"}
} else {
    $results += @{Test="Chat 6.7B"; Status="FAIL"; Details="Falha na resposta complexa"}
}
Write-Host ""

# 5. Teste de Cache (mesma pergunta duas vezes)
Write-Host "5️⃣ TESTE: Sistema de Cache" -ForegroundColor Magenta
$cacheBody = @{
    model = "auto"
    messages = @(
        @{
            role = "user"
            content = "Qual é a capital do Brasil?"
        }
    )
    temperature = 0.7
    max_tokens = 30
}

# Primeira requisição
$start1 = Get-Date
$cache1 = Invoke-ApiTest -Url "$ApiUrl/v1/chat/completions" -Method "POST" -Body $cacheBody -Description "Primeira requisição (sem cache)"
$time1 = ((Get-Date) - $start1).TotalMilliseconds

Start-Sleep -Seconds 2

# Segunda requisição (deve usar cache)
$start2 = Get-Date
$cache2 = Invoke-ApiTest -Url "$ApiUrl/v1/chat/completions" -Method "POST" -Body $cacheBody -Description "Segunda requisição (deve usar cache)"
$time2 = ((Get-Date) - $start2).TotalMilliseconds

if ($cache1 -and $cache2) {
    Write-Host "   Tempo 1ª requisição: $([Math]::Round($time1))ms" -ForegroundColor Cyan
    Write-Host "   Tempo 2ª requisição: $([Math]::Round($time2))ms" -ForegroundColor Cyan
    
    if ($time2 -lt ($time1 * 0.5)) {
        Write-Host "   ✅ Cache funcionando! (2ª req. 50%+ mais rápida)" -ForegroundColor Green
        $results += @{Test="Cache System"; Status="PASS"; Details="Cache acelerou em $([Math]::Round((($time1-$time2)/$time1)*100))%"}
    } else {
        Write-Host "   ⚠️ Cache pode não estar funcionando" -ForegroundColor Yellow
        $results += @{Test="Cache System"; Status="WARNING"; Details="Diferença de tempo não significativa"}
    }
} else {
    $results += @{Test="Cache System"; Status="FAIL"; Details="Erro nas requisições de teste"}
}
Write-Host ""

# 6. Teste de Performance (múltiplas requisições)
Write-Host "6️⃣ TESTE: Performance (5 requisições paralelas)" -ForegroundColor Magenta
$perfBody = @{
    model = "auto"
    messages = @(
        @{
            role = "user"
            content = "Conte até 3 e diga olá."
        }
    )
    temperature = 0.7
    max_tokens = 20
}

$perfStart = Get-Date
$jobs = @()

for ($i = 1; $i -le 5; $i++) {
    $job = Start-Job -ScriptBlock {
        param($Url, $Body)
        try {
            $response = Invoke-RestMethod -Uri $Url -Method POST -Body ($Body | ConvertTo-Json -Depth 3) -ContentType "application/json" -TimeoutSec 30
            return @{Success=$true; Response=$response}
        } catch {
            return @{Success=$false; Error=$_.Exception.Message}
        }
    } -ArgumentList "$ApiUrl/v1/chat/completions", $perfBody
    
    $jobs += $job
}

$jobResults = $jobs | Wait-Job | Receive-Job
$perfEnd = Get-Date
$totalTime = ($perfEnd - $perfStart).TotalSeconds

$successCount = ($jobResults | Where-Object { $_.Success }).Count
Write-Host "   Requisições bem-sucedidas: $successCount/5" -ForegroundColor Cyan
Write-Host "   Tempo total: $([Math]::Round($totalTime, 2))s" -ForegroundColor Cyan
Write-Host "   Tempo médio por requisição: $([Math]::Round($totalTime/5, 2))s" -ForegroundColor Cyan

if ($successCount -ge 4) {
    $results += @{Test="Performance"; Status="PASS"; Details="$successCount/5 requisições paralelas ok"}
} else {
    $results += @{Test="Performance"; Status="FAIL"; Details="Apenas $successCount/5 requisições ok"}
}

# Limpar jobs
$jobs | Remove-Job -Force
Write-Host ""

# 7. Resumo dos Resultados
Write-Host "📊 RESUMO DOS TESTES" -ForegroundColor Magenta
Write-Host "═══════════════════" -ForegroundColor Magenta

$passed = ($results | Where-Object { $_.Status -eq "PASS" }).Count
$failed = ($results | Where-Object { $_.Status -eq "FAIL" }).Count
$warnings = ($results | Where-Object { $_.Status -eq "WARNING" }).Count

foreach ($result in $results) {
    $color = switch ($result.Status) {
        "PASS" { "Green" }
        "FAIL" { "Red" }
        "WARNING" { "Yellow" }
        default { "White" }
    }
    
    Write-Host "   $($result.Status.PadRight(8)) $($result.Test.PadRight(15)) - $($result.Details)" -ForegroundColor $color
}

Write-Host ""
Write-Host "✅ Passou: $passed testes" -ForegroundColor Green
if ($warnings -gt 0) {
    Write-Host "⚠️ Warnings: $warnings testes" -ForegroundColor Yellow
}
if ($failed -gt 0) {
    Write-Host "❌ Falhou: $failed testes" -ForegroundColor Red
}

# Score final
$score = [Math]::Round(($passed / $results.Count) * 100)
Write-Host ""
if ($score -ge 90) {
    Write-Host "🎉 DEPLOYMENT EXCELENTE! Score: $score%" -ForegroundColor Green
} elseif ($score -ge 70) {
    Write-Host "✅ DEPLOYMENT BOM! Score: $score%" -ForegroundColor Cyan
} elseif ($score -ge 50) {
    Write-Host "⚠️ DEPLOYMENT ACEITÁVEL! Score: $score%" -ForegroundColor Yellow
} else {
    Write-Host "❌ DEPLOYMENT COM PROBLEMAS! Score: $score%" -ForegroundColor Red
}

Write-Host ""
Write-Host "🔗 Para monitoramento contínuo:" -ForegroundColor Magenta
Write-Host "   gcloud app logs tail -s llm-api" -ForegroundColor White
Write-Host "   kubectl logs -l app=ollama -f" -ForegroundColor White
