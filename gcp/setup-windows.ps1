# Script PowerShell para setup no Windows para GCP
param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectId,
    
    [string]$Region = "us-central1",
    [string]$Zone = "us-central1-a"
)

Write-Host "🚀 Configurando deployment para Google Cloud Platform..." -ForegroundColor Green
Write-Host "📋 Projeto: $ProjectId" -ForegroundColor Cyan
Write-Host "🌎 Região: $Region" -ForegroundColor Cyan

# Verificar se gcloud está instalado
try {
    $gcloudVersion = gcloud version 2>$null
    Write-Host "✅ Google Cloud CLI encontrado" -ForegroundColor Green
} catch {
    Write-Host "❌ Google Cloud CLI não encontrado. Instale em: https://cloud.google.com/sdk/docs/install" -ForegroundColor Red
    exit 1
}

# Verificar se kubectl está instalado
try {
    $kubectlVersion = kubectl version --client 2>$null
    Write-Host "✅ kubectl encontrado" -ForegroundColor Green
} catch {
    Write-Host "⚠️ kubectl não encontrado. Instalando via gcloud..." -ForegroundColor Yellow
    gcloud components install kubectl
}

# 1. Configurar projeto
Write-Host "🔧 Configurando projeto GCP..." -ForegroundColor Yellow
gcloud config set project $ProjectId
gcloud config set compute/region $Region
gcloud config set compute/zone $Zone

# 2. Fazer login (se necessário)
Write-Host "🔐 Verificando autenticação..." -ForegroundColor Yellow
try {
    $currentAccount = gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>$null
    if (-not $currentAccount) {
        Write-Host "🔐 Fazendo login no Google Cloud..." -ForegroundColor Yellow
        gcloud auth login
        gcloud auth application-default login
    } else {
        Write-Host "✅ Já autenticado como: $currentAccount" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Erro na autenticação" -ForegroundColor Red
    exit 1
}

# 3. Habilitar APIs necessárias
Write-Host "🔌 Habilitando APIs necessárias..." -ForegroundColor Yellow
$apis = @(
    "container.googleapis.com",
    "appengine.googleapis.com", 
    "redis.googleapis.com",
    "compute.googleapis.com"
)

foreach ($api in $apis) {
    Write-Host "   Habilitando $api..." -ForegroundColor Cyan
    gcloud services enable $api
}
Write-Host "✅ APIs habilitadas" -ForegroundColor Green

# 4. Criar diretórios necessários
Write-Host "📁 Criando estrutura de diretórios..." -ForegroundColor Yellow
$dirs = @("gcp", "gcp\terraform")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -Path $dir -ItemType Directory -Force | Out-Null
        Write-Host "   Criado: $dir" -ForegroundColor Cyan
    }
}

# 5. Verificar arquivos necessários
Write-Host "📝 Verificando arquivos de configuração..." -ForegroundColor Yellow
$requiredFiles = @(
    "gcp\app.yaml",
    "gcp\ollama-deployment.yaml", 
    "gcp\deploy.sh",
    "requirements.txt",
    "main.py"
)

$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host "❌ Arquivos faltando:" -ForegroundColor Red
    foreach ($file in $missingFiles) {
        Write-Host "   - $file" -ForegroundColor Red
    }
    Write-Host "Execute o script de criação dos arquivos primeiro." -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Todos os arquivos necessários encontrados" -ForegroundColor Green

# 6. Atualizar configurações com o Project ID
Write-Host "⚙️ Atualizando configurações..." -ForegroundColor Yellow

# Atualizar deploy.sh
if (Test-Path "gcp\deploy.sh") {
    $deployContent = Get-Content "gcp\deploy.sh" -Raw
    $deployContent = $deployContent -replace 'PROJECT_ID="your-gcp-project-id"', "PROJECT_ID=`"$ProjectId`""
    $deployContent = $deployContent -replace 'REGION="us-central1"', "REGION=`"$Region`""
    $deployContent = $deployContent -replace 'ZONE="us-central1-a"', "ZONE=`"$Zone`""
    Set-Content "gcp\deploy.sh" $deployContent -Encoding UTF8
}

# 7. Testar conectividade
Write-Host "🧪 Testando conectividade..." -ForegroundColor Yellow
try {
    $projectInfo = gcloud projects describe $ProjectId --format="value(projectId)" 2>$null
    if ($projectInfo -eq $ProjectId) {
        Write-Host "✅ Projeto acessível: $ProjectId" -ForegroundColor Green
    } else {
        Write-Host "❌ Não foi possível acessar o projeto: $ProjectId" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Erro ao verificar projeto" -ForegroundColor Red
    exit 1
}

# 8. Estimar custos
Write-Host "" 
Write-Host "💰 Estimativa de custos mensais (USD):" -ForegroundColor Yellow
Write-Host "   GKE Cluster (CPU): ~`$75" -ForegroundColor Cyan
Write-Host "   GPU Node Pool (T4): ~`$150" -ForegroundColor Cyan  
Write-Host "   App Engine: ~`$25-100" -ForegroundColor Cyan
Write-Host "   Redis (Memorystore): ~`$45" -ForegroundColor Cyan
Write-Host "   Armazenamento: ~`$10" -ForegroundColor Cyan
Write-Host "   ─────────────────────────" -ForegroundColor DarkGray
Write-Host "   Total estimado: ~`$305-380/mês" -ForegroundColor Yellow

# 9. Próximos passos
Write-Host ""
Write-Host "✅ Setup inicial completo!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Próximos passos:" -ForegroundColor Yellow
Write-Host "   1. Para deploy automatizado:" -ForegroundColor White
Write-Host "      bash gcp/deploy.sh" -ForegroundColor Cyan
Write-Host ""
Write-Host "   2. Para deploy com Terraform:" -ForegroundColor White  
Write-Host "      cd gcp/terraform" -ForegroundColor Cyan
Write-Host "      terraform init" -ForegroundColor Cyan
Write-Host "      terraform apply -var=`"project_id=$ProjectId`"" -ForegroundColor Cyan
Write-Host ""
Write-Host "   3. Para monitorar deployment:" -ForegroundColor White
Write-Host "      gcloud app logs tail -s llm-api" -ForegroundColor Cyan
Write-Host ""
Write-Host "📚 Documentação completa em: gcp/README.md" -ForegroundColor Magenta

# 10. Salvar configuração
$configFile = "gcp\.gcp-config.json"
$config = @{
    project_id = $ProjectId
    region = $Region
    zone = $Zone
    setup_date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
} | ConvertTo-Json -Depth 2

Set-Content $configFile $config -Encoding UTF8
Write-Host "💾 Configuração salva em: $configFile" -ForegroundColor Green
