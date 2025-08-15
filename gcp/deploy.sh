#!/bin/bash
# Script de deployment para Google Cloud Platform
set -e

echo "🚀 Iniciando deployment no Google Cloud Platform..."

# Configurações
PROJECT_ID="your-gcp-project-id"
REGION="us-central1"
ZONE="us-central1-a"
CLUSTER_NAME="llm-deepseek-cluster"
APP_NAME="llm-api"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}🔄 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 1. Configurar projeto
print_step "Configurando projeto GCP..."
gcloud config set project $PROJECT_ID
gcloud config set compute/region $REGION
gcloud config set compute/zone $ZONE

# 2. Habilitar APIs necessárias
print_step "Habilitando APIs necessárias..."
gcloud services enable container.googleapis.com
gcloud services enable appengine.googleapis.com
gcloud services enable redis.googleapis.com
gcloud services enable compute.googleapis.com
print_success "APIs habilitadas"

# 3. Criar cluster GKE com GPUs para Ollama
print_step "Criando cluster GKE com suporte a GPU..."
gcloud container clusters create $CLUSTER_NAME \
    --zone=$ZONE \
    --machine-type=e2-standard-4 \
    --num-nodes=1 \
    --enable-autorepair \
    --enable-autoupgrade \
    --enable-autoscaling \
    --min-nodes=1 \
    --max-nodes=3

# Criar node pool com GPU para Ollama
print_step "Criando node pool com GPU..."
gcloud container node-pools create gpu-pool \
    --cluster=$CLUSTER_NAME \
    --zone=$ZONE \
    --machine-type=n1-standard-4 \
    --accelerator=type=nvidia-tesla-t4,count=1 \
    --num-nodes=1 \
    --enable-autorepair \
    --enable-autoupgrade \
    --enable-autoscaling \
    --min-nodes=0 \
    --max-nodes=2

print_success "Cluster GKE criado com sucesso"

# 4. Configurar kubectl
print_step "Configurando kubectl..."
gcloud container clusters get-credentials $CLUSTER_NAME --zone=$ZONE
print_success "kubectl configurado"

# 5. Instalar NVIDIA device plugin
print_step "Instalando NVIDIA device plugin..."
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/master/nvidia-driver-installer/cos/daemonset-preloaded.yaml

# 6. Criar Redis instance (Memorystore)
print_step "Criando instância Redis..."
gcloud redis instances create llm-redis \
    --size=1 \
    --region=$REGION \
    --redis-version=redis_6_x \
    --tier=standard || print_warning "Redis instance já existe ou erro na criação"

# 7. Deploy Ollama no GKE
print_step "Fazendo deploy do Ollama..."
kubectl apply -f gcp/ollama-deployment.yaml
print_success "Ollama deployed"

# 8. Aguardar Ollama estar ready
print_step "Aguardando Ollama ficar pronto..."
kubectl wait --for=condition=ready pod -l app=ollama --timeout=300s

# 9. Fazer pull dos modelos DeepSeek
print_step "Baixando modelos DeepSeek..."
OLLAMA_POD=$(kubectl get pods -l app=ollama -o jsonpath='{.items[0].metadata.name}')

kubectl exec $OLLAMA_POD -- ollama pull deepseek-coder:1.3b
kubectl exec $OLLAMA_POD -- ollama pull deepseek-coder:6.7b
print_success "Modelos DeepSeek baixados"

# 10. Preparar aplicação para App Engine
print_step "Preparando aplicação para App Engine..."

# Criar requirements.txt se não existir
if [ ! -f requirements.txt ]; then
cat > requirements.txt << EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.4.2
aiohttp==3.8.6
redis==5.0.1
sentence-transformers==2.2.2
numpy==1.24.4
requests==2.31.0
python-multipart==0.0.6
EOF
fi

# Criar main.py para App Engine
if [ ! -f main.py ]; then
cat > main.py << EOF
from src.simple_llm_server import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
EOF
fi

print_success "Arquivos preparados"

# 11. Deploy da API no App Engine
print_step "Fazendo deploy da API no App Engine..."

# Obter IP interno do Redis
REDIS_IP=$(gcloud redis instances describe llm-redis --region=$REGION --format="value(host)")
print_step "Redis IP: $REDIS_IP"

# Atualizar app.yaml com IP do Redis
sed -i "s/10.0.0.1/$REDIS_IP/g" gcp/app.yaml

# Deploy
gcloud app deploy gcp/app.yaml --quiet
print_success "API deployed no App Engine"

# 12. Obter URLs
print_step "Obtendo informações de deployment..."
APP_URL=$(gcloud app browse --no-launch-browser 2>/dev/null | grep "https://")
OLLAMA_IP=$(kubectl get service ollama-service -o jsonpath='{.spec.clusterIP}')

print_success "🎉 Deployment concluído com sucesso!"
echo ""
echo -e "${GREEN}📋 Informações do deployment:${NC}"
echo -e "${BLUE}🤖 API URL: ${APP_URL}${NC}"
echo -e "${BLUE}🧠 Ollama Internal IP: ${OLLAMA_IP}:11434${NC}"
echo -e "${BLUE}🔴 Redis IP: ${REDIS_IP}:6379${NC}"
echo ""
echo -e "${YELLOW}📋 Próximos passos:${NC}"
echo "1. Configure o DNS/Load Balancer se necessário"
echo "2. Configure monitoramento e logs"
echo "3. Configure backup dos modelos"
echo "4. Teste a API: curl $APP_URL/v1/models"

# 13. Teste básico
print_step "Executando teste básico..."
curl -s "$APP_URL/" | grep -q "running" && print_success "API está respondendo!" || print_warning "API pode não estar respondendo corretamente"

echo -e "${GREEN}🚀 Setup completo no Google Cloud!${NC}"
