# Guia de Deploy no Google Cloud Vertex AI

Este guia mostra como fazer o deploy do sistema LLM com DeepSeek no Google Cloud Platform.

## 📋 Pré-requisitos

1. **Conta Google Cloud** com faturamento ativado
2. **gcloud CLI** instalado e configurado
3. **kubectl** instalado
4. **Docker** instalado (para testes locais)
5. **Terraform** instalado (opcional, para infraestrutura como código)

## 🚀 Opções de Deploy

### Opção 1: Deploy Automatizado (Recomendado)

```bash
# 1. Configure suas variáveis
export PROJECT_ID="seu-projeto-gcp"
export REGION="us-central1"

# 2. Execute o script de deploy
chmod +x gcp/deploy.sh
./gcp/deploy.sh
```

### Opção 2: Deploy com Terraform

```bash
# 1. Entre no diretório terraform
cd gcp/terraform

# 2. Inicialize o Terraform
terraform init

# 3. Planeje o deploy
terraform plan -var="project_id=seu-projeto-gcp"

# 4. Execute o deploy
terraform apply -var="project_id=seu-projeto-gcp"
```

### Opção 3: Deploy Manual

#### 1. Configurar projeto
```bash
gcloud config set project SEU-PROJETO-ID
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a
```

#### 2. Habilitar APIs
```bash
gcloud services enable container.googleapis.com
gcloud services enable appengine.googleapis.com
gcloud services enable redis.googleapis.com
```

#### 3. Criar cluster GKE
```bash
# Cluster principal
gcloud container clusters create llm-deepseek-cluster \
    --zone=us-central1-a \
    --machine-type=e2-standard-4 \
    --num-nodes=1

# Node pool com GPU para Ollama
gcloud container node-pools create gpu-pool \
    --cluster=llm-deepseek-cluster \
    --zone=us-central1-a \
    --machine-type=n1-standard-4 \
    --accelerator=type=nvidia-tesla-t4,count=1 \
    --num-nodes=1
```

#### 4. Deploy Ollama
```bash
kubectl apply -f gcp/ollama-deployment.yaml
```

#### 5. Instalar modelos DeepSeek
```bash
# Aguardar pod ficar pronto
kubectl wait --for=condition=ready pod -l app=ollama --timeout=300s

# Instalar modelos
OLLAMA_POD=$(kubectl get pods -l app=ollama -o jsonpath='{.items[0].metadata.name}')
kubectl exec $OLLAMA_POD -- ollama pull deepseek-coder:1.3b
kubectl exec $OLLAMA_POD -- ollama pull deepseek-coder:6.7b
```

#### 6. Criar Redis
```bash
gcloud redis instances create llm-redis \
    --size=1 \
    --region=us-central1 \
    --redis-version=redis_6_x
```

#### 7. Deploy da API
```bash
# Atualizar app.yaml com IP do Redis
REDIS_IP=$(gcloud redis instances describe llm-redis --region=us-central1 --format="value(host)")

# Deploy no App Engine
gcloud app deploy gcp/app.yaml
```

## 🏗️ Arquitetura no GCP

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   App Engine    │    │   GKE Cluster    │    │  Memorystore    │
│   (API Server)  │◄──►│  (Ollama+GPU)    │    │   (Redis)       │
│                 │    │                  │    │                 │
│ - FastAPI       │    │ - DeepSeek 1.3B  │    │ - Semantic      │
│ - Auto-scaling  │    │ - DeepSeek 6.7B  │    │   Cache         │
│ - Load Balancer │    │ - NVIDIA T4      │    │ - High Avail.   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 💰 Estimativa de Custos (USD/mês)

### Configuração Mínima
- **GKE Cluster**: ~$75/mês
- **GPU Node (T4)**: ~$150/mês
- **App Engine**: ~$25/mês (tráfego baixo)
- **Memorystore Redis**: ~$45/mês
- **Armazenamento**: ~$10/mês
- **Total**: ~$305/mês

### Configuração Produção
- **GKE Cluster**: ~$200/mês (múltiplos nodes)
- **GPU Nodes**: ~$300/mês (2x T4)
- **App Engine**: ~$100/mês (tráfego médio)
- **Memorystore Redis**: ~$90/mês (HA)
- **Load Balancer**: ~$18/mês
- **Total**: ~$708/mês

## 🔧 Configurações Recomendadas

### Para Desenvolvimento
```yaml
# Menores recursos para testes
GKE: e2-small nodes
GPU: 1x nvidia-tesla-t4
Redis: 1GB Standard
App Engine: F1 instances
```

### Para Produção
```yaml
# Recursos otimizados
GKE: e2-standard-4 nodes
GPU: 2x nvidia-tesla-t4 (HA)
Redis: 4GB Standard HA
App Engine: F4_1G instances
Load Balancer: HTTP(S) LB
```

## 📊 Monitoramento

### Métricas Importantes
- **Latência da API**: < 2s para DeepSeek 1.3B
- **Taxa de Cache Hit**: > 60%
- **Uso de GPU**: 70-90% durante inferência
- **Memória Ollama**: < 12GB por modelo

### Logs Importantes
```bash
# Logs da API
gcloud app logs tail -s llm-api

# Logs do Ollama
kubectl logs -l app=ollama -f

# Métricas do cluster
kubectl top nodes
kubectl top pods
```

## 🔒 Segurança

### Configurações Obrigatórias
1. **Firewall Rules**: Apenas portas necessárias
2. **API Key**: Configurar chave segura
3. **VPC**: Rede privada para componentes internos
4. **IAM**: Princípio do menor privilégio
5. **Encryption**: Dados em trânsito e repouso

### Exemplo de configuração IAM
```bash
# Service Account para App Engine
gcloud iam service-accounts create llm-api-sa \
    --display-name="LLM API Service Account"

# Permissions mínimas
gcloud projects add-iam-policy-binding YOUR-PROJECT-ID \
    --member="serviceAccount:llm-api-sa@YOUR-PROJECT-ID.iam.gserviceaccount.com" \
    --role="roles/redis.editor"
```

## 🎯 Otimizações de Performance

### Auto-scaling
```yaml
# App Engine - app.yaml
automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.6

# GKE - HPA
kubectl autoscale deployment ollama-deepseek \
    --cpu-percent=70 --min=1 --max=3
```

### Cache Strategy
- **TTL**: 5 minutos para respostas similares
- **Similarity Threshold**: 0.85 para cache semântico
- **Redis Memory**: Configurar eviction policy LRU

## 🆘 Troubleshooting

### Problemas Comuns

#### 1. Ollama não carrega modelos
```bash
# Verificar espaço em disco
kubectl exec -it $OLLAMA_POD -- df -h

# Verificar logs
kubectl logs $OLLAMA_POD

# Reinstalar modelo
kubectl exec $OLLAMA_POD -- ollama pull deepseek-coder:1.3b
```

#### 2. API lenta
```bash
# Verificar cache hit rate
# No Redis: INFO stats

# Verificar CPU/Memory
kubectl top pods -l app=ollama

# Verificar latência da rede
curl -w "@curl-format.txt" https://YOUR-APP.appspot.com/
```

#### 3. GPU não detectada
```bash
# Verificar drivers NVIDIA
kubectl describe nodes

# Verificar device plugin
kubectl get daemonset -n kube-system

# Reinstalar drivers
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/master/nvidia-driver-installer/cos/daemonset-preloaded.yaml
```

## 📞 Suporte

Para questões específicas do GCP:
- [Google Cloud Documentation](https://cloud.google.com/docs)
- [GKE Troubleshooting](https://cloud.google.com/kubernetes-engine/docs/troubleshooting)
- [App Engine Troubleshooting](https://cloud.google.com/appengine/docs/standard/python3/troubleshooting)

## 🔄 Updates e Manutenção

### Deploy de Atualizações
```bash
# Atualizar API
gcloud app deploy gcp/app.yaml --version=v2

# Atualizar Ollama
kubectl set image deployment/ollama-deepseek ollama=ollama/ollama:latest

# Rolling update sem downtime
kubectl rollout restart deployment/ollama-deepseek
```

### Backup dos Modelos
```bash
# Criar snapshot do PVC
kubectl create snapshot ollama-models-snapshot \
    --claim-name=ollama-models-pvc

# Ou backup para GCS
kubectl exec $OLLAMA_POD -- tar -czf - /root/.ollama | \
    gsutil cp - gs://your-backup-bucket/ollama-models-backup.tar.gz
```
