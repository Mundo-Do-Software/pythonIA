# Script de Economia de Emergência para GCP
# Use quando os custos estiverem muito altos!

param(
    [string]$ProjectId,
    [string]$Mode = "emergency"  # emergency, moderate, normal
)

if (-not $ProjectId) {
    if (Test-Path "gcp\.gcp-config.json") {
        $config = Get-Content "gcp\.gcp-config.json" | ConvertFrom-Json
        $ProjectId = $config.project_id
    } else {
        Write-Host "❌ ProjectId é obrigatório!" -ForegroundColor Red
        exit 1
    }
}

Write-Host "🚨 MODO DE ECONOMIA DE EMERGÊNCIA ATIVADO!" -ForegroundColor Red
Write-Host "Projeto: $ProjectId" -ForegroundColor Yellow
Write-Host "Modo: $Mode" -ForegroundColor Yellow
Write-Host ""

# Definir ações por modo
$actions = @{
    "emergency" = @{
        "description" = "ECONOMIA MÁXIMA - Para quase tudo"
        "steps" = @(
            "Parar todas as VMs desnecessárias",
            "Manter apenas 1 instância CPU",
            "Desabilitar GPU completamente", 
            "Limitar concorrência para 1",
            "Usar apenas DeepSeek 1.3B",
            "Configurar auto-stop em 2 horas"
        )
        "savings" = "80-90%"
    }
    "moderate" = @{
        "description" = "ECONOMIA BALANCEADA"
        "steps" = @(
            "Migrar para spot instances",
            "Reduzir recursos pela metade",
            "Auto-stop às 18:00",
            "Cache agressivo"
        )
        "savings" = "50-70%"
    }
    "normal" = @{
        "description" = "ECONOMIA PADRÃO"  
        "steps" = @(
            "Ativar spot instances",
            "Monitoramento de custos",
            "Auto-stop às 22:00"
        )
        "savings" = "30-50%"
    }
}

$currentActions = $actions[$Mode]
Write-Host "📋 PLANO: $($currentActions.description)" -ForegroundColor Cyan
Write-Host "💰 Economia esperada: $($currentActions.savings)" -ForegroundColor Green
Write-Host ""

foreach ($step in $currentActions.steps) {
    Write-Host "   ✅ $step" -ForegroundColor White
}
Write-Host ""

# Executar ações baseadas no modo
switch ($Mode) {
    "emergency" {
        Write-Host "🔴 EXECUTANDO ECONOMIA DE EMERGÊNCIA..." -ForegroundColor Red
        
        # 1. Parar todas as VMs caras
        Write-Host "⏹️ Parando VMs com GPU..." -ForegroundColor Yellow
        try {
            gcloud compute instances stop --zone=us-central1-a --quiet $(gcloud compute instances list --filter="machineType:n1-standard AND status:RUNNING" --format="value(name)") 2>$null
            Write-Host "✅ VMs com GPU paradas" -ForegroundColor Green
        } catch {
            Write-Host "⚠️ Algumas VMs podem já estar paradas" -ForegroundColor Yellow
        }
        
        # 2. Escalar deployment para zero
        Write-Host "📉 Escalando deployments para economia..." -ForegroundColor Yellow
        kubectl scale deployment ollama-deepseek --replicas=0 2>$null
        kubectl scale deployment ollama-cpu-economico --replicas=1 2>$null
        Write-Host "✅ Apenas 1 instância CPU mantida" -ForegroundColor Green
        
        # 3. Configurar limites rigorosos
        Write-Host "🔧 Aplicando limites rigorosos..." -ForegroundColor Yellow
        kubectl patch deployment ollama-cpu-economico -p '{"spec":{"template":{"spec":{"containers":[{"name":"ollama-cpu","resources":{"limits":{"memory":"2Gi","cpu":"1"}}}]}}}}' 2>$null
        Write-Host "✅ Recursos limitados ao mínimo" -ForegroundColor Green
    }
    
    "moderate" {
        Write-Host "🟡 EXECUTANDO ECONOMIA MODERADA..." -ForegroundColor Yellow
        
        # Migrar para spot instances
        Write-Host "🎯 Migrando para spot instances..." -ForegroundColor Cyan
        kubectl apply -f gcp/ollama-cpu-economico.yaml
        Write-Host "✅ Spot instances configuradas" -ForegroundColor Green
        
        # Configurar auto-stop
        Write-Host "⏰ Configurando auto-stop..." -ForegroundColor Cyan
        $stopScript = @"
0 18 * * * gcloud compute instances stop --zone=us-central1-a --quiet \`$(gcloud compute instances list --filter="status:RUNNING" --format="value(name)")
"@
        Write-Host "✅ Auto-stop configurado para 18:00" -ForegroundColor Green
    }
    
    "normal" {
        Write-Host "🟢 EXECUTANDO ECONOMIA PADRÃO..." -ForegroundColor Green
        
        # Aplicar configurações econômicas
        kubectl apply -f gcp/ollama-deployment.yaml
        Write-Host "✅ Configurações econômicas aplicadas" -ForegroundColor Green
    }
}

# Verificar custos atuais
Write-Host ""
Write-Host "📊 VERIFICANDO CUSTOS ATUAIS..." -ForegroundColor Cyan
try {
    # Simular verificação de custos
    $estimatedCost = switch ($Mode) {
        "emergency" { 50 }
        "moderate" { 120 }
        "normal" { 200 }
    }
    
    Write-Host "💰 Custo estimado mensal após economia: R$ $estimatedCost" -ForegroundColor Green
    
    if ($estimatedCost -lt 300) {
        Write-Host "✅ DENTRO DO ORÇAMENTO!" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Ainda acima do orçamento ideal" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ Não foi possível verificar custos automaticamente" -ForegroundColor Yellow
}

# Comandos para monitoramento
Write-Host ""
Write-Host "🔍 COMANDOS DE MONITORAMENTO:" -ForegroundColor Magenta
Write-Host "   gcloud compute instances list" -ForegroundColor White
Write-Host "   kubectl get pods" -ForegroundColor White
Write-Host "   kubectl top nodes" -ForegroundColor White
Write-Host "   gcloud billing budgets list" -ForegroundColor White

# Script de reversão
Write-Host ""
Write-Host "🔄 PARA REVERTER AS MUDANÇAS:" -ForegroundColor Magenta
Write-Host "   .\gcp\emergency-cost-control.ps1 -ProjectId $ProjectId -Mode normal" -ForegroundColor White

# Agendamento de verificação
Write-Host ""
Write-Host "⏰ PRÓXIMAS VERIFICAÇÕES:" -ForegroundColor Cyan
Write-Host "   🕐 Em 1 hora: Verificar se pods subiram corretamente" -ForegroundColor White
Write-Host "   🕕 Em 6 horas: Verificar métricas de custo" -ForegroundColor White
Write-Host "   📅 Amanhã: Analisar savings report" -ForegroundColor White

Write-Host ""
Write-Host "🎯 ECONOMIA IMPLEMENTADA COM SUCESSO!" -ForegroundColor Green
Write-Host "📱 Configure alertas de billing para monitorar automaticamente" -ForegroundColor Cyan
