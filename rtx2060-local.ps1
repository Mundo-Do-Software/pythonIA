# Script PowerShell para teste local com RTX 2060
param(
    [switch]$Setup,
    [switch]$Start,
    [switch]$Stop,
    [switch]$Test,
    [switch]$Monitor,
    [switch]$Clean
)

Write-Host "🎮 Configuração Local RTX 2060 - DeepSeek" -ForegroundColor Green

# Verificar Docker e NVIDIA Docker
function Test-Prerequisites {
    Write-Host "🔍 Verificando pré-requisitos..." -ForegroundColor Yellow
    
    # Docker
    try {
        $dockerVersion = docker --version 2>$null
        if ($dockerVersion) {
            Write-Host "✅ Docker: $dockerVersion" -ForegroundColor Green
        } else {
            throw "Docker não encontrado"
        }
    } catch {
        Write-Host "❌ Docker não encontrado! Instale em: https://docker.com" -ForegroundColor Red
        return $false
    }
    
    # NVIDIA Docker - teste simples
    try {
        $nvidiaTest = nvidia-smi 2>$null
        if ($nvidiaTest) {
            Write-Host "✅ NVIDIA Docker disponível" -ForegroundColor Green
        } else {
            throw "NVIDIA não encontrado"
        }
    } catch {
        Write-Host "❌ NVIDIA Docker não configurado!" -ForegroundColor Red
        Write-Host "💡 Instale NVIDIA Docker: https://github.com/NVIDIA/nvidia-docker" -ForegroundColor Yellow
        return $false
    }
    
    return $true
}

function Start-LocalSetup {
    Write-Host "🚀 Iniciando setup local..." -ForegroundColor Cyan
    
    if (-not (Test-Prerequisites)) {
        return
    }
    
    # Criar diretórios necessários
    $dirs = @("models", "config", "logs")
    foreach ($dir in $dirs) {
        if (-not (Test-Path $dir)) {
            New-Item -Path $dir -ItemType Directory -Force | Out-Null
            Write-Host "📁 Criado: $dir" -ForegroundColor Cyan
        }
    }
    
    # Baixar modelos DeepSeek
    Write-Host "📥 Iniciando containers..." -ForegroundColor Yellow
    docker-compose -f docker-compose.local.yml up -d ollama-local redis-local
    
    Start-Sleep -Seconds 15
    
    Write-Host "📥 Baixando DeepSeek 1.3B (otimizado para RTX 2060)..." -ForegroundColor Yellow
    docker exec ollama-rtx2060 ollama pull deepseek-coder:1.3b
    
    Write-Host "✅ Setup local concluído!" -ForegroundColor Green
}

function Start-LocalServices {
    Write-Host "▶️ Iniciando serviços locais..." -ForegroundColor Cyan
    
    # Verificar uso de VRAM antes
    Write-Host "📊 Verificando VRAM disponível..." -ForegroundColor Yellow
    try {
        $gpuInfo = nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits
        if ($gpuInfo) {
            $mem = $gpuInfo.Split(",")
            $used = [int]$mem[0].Trim()
            $total = [int]$mem[1].Trim()
            $available = $total - $used
            
            Write-Host "🎮 RTX 2060: $used MB usado / $total MB total" -ForegroundColor Cyan
            Write-Host "💾 Disponível: $available MB" -ForegroundColor Green
            
            if ($available -lt 3000) {
                Write-Host "⚠️ VRAM baixa! Feche outros programas que usam GPU" -ForegroundColor Yellow
            }
        }
    } catch {
        Write-Host "⚠️ Não foi possível verificar VRAM" -ForegroundColor Yellow
    }
    
    # Iniciar todos os serviços
    docker-compose -f docker-compose.local.yml up -d
    
    Start-Sleep -Seconds 10
    
    # Verificar status
    Write-Host "🔍 Verificando serviços..." -ForegroundColor Yellow
    
    # Testar Ollama
    try {
        $ollamaResponse = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -TimeoutSec 5
        Write-Host "✅ Ollama: Online" -ForegroundColor Green
    } catch {
        Write-Host "❌ Ollama: Offline" -ForegroundColor Red
    }
    
    # Testar API
    try {
        $apiResponse = Invoke-RestMethod -Uri "http://localhost:5000/" -TimeoutSec 5
        Write-Host "✅ API: Online" -ForegroundColor Green
    } catch {
        Write-Host "❌ API: Offline" -ForegroundColor Red
    }
    
    # Testar Redis (verificar porta)
    $redisPort = netstat -an | Select-String ":6379"
    if ($redisPort) {
        Write-Host "✅ Redis: Online (porta 6379)" -ForegroundColor Green
    } else {
        Write-Host "❌ Redis: Offline" -ForegroundColor Red
    }
    
    Write-Host "`n🌐 Serviços disponíveis:" -ForegroundColor Magenta
    Write-Host "   Ollama: http://localhost:11434" -ForegroundColor White
    Write-Host "   API: http://localhost:5000" -ForegroundColor White
    Write-Host "   Redis: localhost:6379" -ForegroundColor White
}

function Test-LocalDeployment {
    Write-Host "🧪 Executando testes locais..." -ForegroundColor Cyan
    
    # Teste 1: Health check
    Write-Host "`n1️⃣ Teste: Health Check API" -ForegroundColor Yellow
    try {
        $health = Invoke-RestMethod -Uri "http://localhost:5000/" -TimeoutSec 10
        Write-Host "✅ API Status: OK" -ForegroundColor Green
    } catch {
        Write-Host "❌ API não está respondendo" -ForegroundColor Red
    }
    
    # Teste 2: Modelos disponíveis
    Write-Host "`n2️⃣ Teste: Modelos Disponíveis" -ForegroundColor Yellow
    try {
        $models = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -TimeoutSec 10
        Write-Host "✅ Modelos encontrados:" -ForegroundColor Green
        foreach ($model in $models.models) {
            $sizeGB = [math]::Round($model.size / 1GB, 2)
            Write-Host "   - $($model.name) ($sizeGB GB)" -ForegroundColor Cyan
        }
    } catch {
        Write-Host "❌ Não foi possível listar modelos" -ForegroundColor Red
    }
    
    # Teste 3: Inferência simples (RTX 2060)
    Write-Host "`n3️⃣ Teste: Inferência RTX 2060" -ForegroundColor Yellow
    $testPrompt = @{
        model = "auto"
        messages = @(
            @{
                role = "user"
                content = "Olá! Você está rodando em uma RTX 2060. Responda brevemente."
            }
        )
        temperature = 0.7
        max_tokens = 50
    } | ConvertTo-Json -Depth 3
    
    $startTime = Get-Date
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:5000/v1/chat/completions" -Method POST -Body $testPrompt -ContentType "application/json" -TimeoutSec 30
        $endTime = Get-Date
        $duration = ($endTime - $startTime).TotalSeconds
        
        Write-Host "✅ Inferência bem-sucedida!" -ForegroundColor Green
        Write-Host "   Tempo: $([math]::Round($duration, 2))s" -ForegroundColor Cyan
        
        if ($response.choices -and $response.choices[0].message) {
            Write-Host "   Resposta: $($response.choices[0].message.content)" -ForegroundColor White
        }
        
        # Performance benchmark
        if ($duration -lt 5) {
            Write-Host "🚀 Performance: Excelente (<5s)" -ForegroundColor Green
        } elseif ($duration -lt 10) {
            Write-Host "✅ Performance: Boa (5-10s)" -ForegroundColor Yellow
        } else {
            Write-Host "⚠️ Performance: Lenta (>10s) - Verifique VRAM" -ForegroundColor Red
        }
        
    } catch {
        Write-Host "❌ Erro na inferência: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Teste 4: Monitoramento VRAM
    Write-Host "`n4️⃣ Teste: Uso de VRAM pós-inferência" -ForegroundColor Yellow
    try {
        $gpuStats = nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits
        if ($gpuStats) {
            $data = $gpuStats.Split(",")
            $memUsed = [int]$data[0].Trim()
            $memTotal = [int]$data[1].Trim()
            $gpuUtil = [int]$data[2].Trim()
            
            $memPercent = [math]::Round($memUsed * 100.0 / $memTotal, 1)
            Write-Host "📊 VRAM: $memUsed/$memTotal MB ($memPercent%)" -ForegroundColor Cyan
            Write-Host "📊 GPU Utilization: $gpuUtil%" -ForegroundColor Cyan
            
            if ($memUsed -gt 5500) {
                Write-Host "⚠️ VRAM alta! Considere reduzir context_length" -ForegroundColor Yellow
            }
        }
    } catch {
        Write-Host "⚠️ Não foi possível verificar VRAM" -ForegroundColor Yellow
    }
}

function Show-ResourceMonitor {
    Write-Host "📊 Monitor de Recursos RTX 2060" -ForegroundColor Cyan
    Write-Host "Pressione Ctrl+C para sair..." -ForegroundColor Yellow
    
    while ($true) {
        Clear-Host
        Write-Host "📊 MONITOR RTX 2060 - $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Green
        Write-Host "══════════════════════════════════════════════════" -ForegroundColor Gray
        
        # GPU Stats
        try {
            $gpuData = nvidia-smi --query-gpu=name,temperature.gpu,memory.used,memory.total,utilization.gpu,power.draw --format=csv,noheader,nounits
            if ($gpuData) {
                $data = $gpuData.Split(",")
                $name = $data[0].Trim()
                $temp = $data[1].Trim()
                $memUsed = [int]$data[2].Trim()
                $memTotal = [int]$data[3].Trim()
                $gpuUtil = [int]$data[4].Trim()
                $power = $data[5].Trim()
                
                $memPercent = [math]::Round($memUsed * 100.0 / $memTotal, 1)
                
                Write-Host "🎮 GPU: $name" -ForegroundColor Cyan
                Write-Host "🌡️  Temperatura: $temp°C" -ForegroundColor White
                Write-Host "💾 VRAM: $memUsed/$memTotal MB ($memPercent%)" -ForegroundColor White
                Write-Host "⚡ Utilização: $gpuUtil%" -ForegroundColor White
                Write-Host "🔌 Energia: $power W" -ForegroundColor White
            }
        } catch {
            Write-Host "❌ Erro ao ler dados da GPU" -ForegroundColor Red
        }
        
        Write-Host ""
        
        # CPU e RAM do sistema
        try {
            $cpu = Get-WmiObject win32_processor | Measure-Object -property LoadPercentage -Average
            $memory = Get-WmiObject -class win32_operatingsystem
            $memoryUsed = [math]::Round(($memory.TotalVisibleMemorySize - $memory.FreePhysicalMemory) * 100.0 / $memory.TotalVisibleMemorySize, 1)
            
            Write-Host "💻 CPU: $([math]::Round($cpu.Average, 1))%" -ForegroundColor White
            Write-Host "🧠 RAM: $memoryUsed%" -ForegroundColor White
        } catch {
            Write-Host "❌ Erro ao ler dados do sistema" -ForegroundColor Red
        }
        
        # Status dos containers
        Write-Host ""
        Write-Host "📦 Containers:" -ForegroundColor Yellow
        try {
            $containers = docker ps --filter "name=rtx2060" --format "table {{.Names}}\t{{.Status}}"
            if ($containers) {
                $containers | ForEach-Object {
                    if ($_ -notlike "*NAMES*") {
                        Write-Host "   $_" -ForegroundColor White
                    }
                }
            } else {
                Write-Host "   Nenhum container RTX 2060 encontrado" -ForegroundColor Gray
            }
        } catch {
            Write-Host "   ❌ Erro ao verificar containers" -ForegroundColor Red
        }
        
        Write-Host "`n❌ Pressione Ctrl+C para sair" -ForegroundColor DarkGray
        Start-Sleep -Seconds 2
    }
}

function Stop-LocalServices {
    Write-Host "⏹️ Parando serviços locais..." -ForegroundColor Yellow
    docker-compose -f docker-compose.local.yml down
    Write-Host "✅ Serviços parados" -ForegroundColor Green
}

function Remove-LocalEnvironment {
    Write-Host "🧹 Limpando ambiente local..." -ForegroundColor Yellow
    
    # Parar e remover containers
    docker-compose -f docker-compose.local.yml down -v --remove-orphans
    
    # Remover imagens locais (opcional)
    Write-Host "🗑️ Deseja remover imagens Docker? (y/N): " -ForegroundColor Yellow -NoNewline
    $response = Read-Host
    if ($response -eq "y" -or $response -eq "Y") {
        docker rmi ollama-rtx2060 llm-api-rtx2060 2>$null
    }
    
    # Limpar cache de modelos (opcional)  
    Write-Host "🗑️ Deseja limpar cache de modelos? (y/N): " -ForegroundColor Yellow -NoNewline
    $response = Read-Host
    if ($response -eq "y" -or $response -eq "Y") {
        Remove-Item -Path "models" -Recurse -Force -ErrorAction SilentlyContinue
    }
    
    Write-Host "✅ Limpeza concluída" -ForegroundColor Green
}

# Executar ações baseadas nos parâmetros
if ($Setup) { Start-LocalSetup }
if ($Start) { Start-LocalServices }
if ($Stop) { Stop-LocalServices }
if ($Test) { Test-LocalDeployment }
if ($Monitor) { Show-ResourceMonitor }
if ($Clean) { Remove-LocalEnvironment }

# Se nenhum parâmetro for fornecido, mostrar ajuda
if (-not ($Setup -or $Start -or $Stop -or $Test -or $Monitor -or $Clean)) {
    Write-Host ""
    Write-Host "🎮 RTX 2060 Local Setup - Comandos Disponíveis:" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "  .\rtx2060-local.ps1 -Setup    - Configuração inicial" -ForegroundColor White
    Write-Host "  .\rtx2060-local.ps1 -Start    - Iniciar serviços" -ForegroundColor White
    Write-Host "  .\rtx2060-local.ps1 -Test     - Executar testes" -ForegroundColor White
    Write-Host "  .\rtx2060-local.ps1 -Monitor  - Monitor em tempo real" -ForegroundColor White
    Write-Host "  .\rtx2060-local.ps1 -Stop     - Parar serviços" -ForegroundColor White
    Write-Host "  .\rtx2060-local.ps1 -Clean    - Limpar ambiente" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Exemplo: .\rtx2060-local.ps1 -Setup -Start -Test" -ForegroundColor Yellow
    Write-Host ""
}
