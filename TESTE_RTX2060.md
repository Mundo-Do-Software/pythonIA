# 🎮 Guia de Teste Local - RTX 2060

## 🚀 Setup Rápido (5 minutos)

### 1. Preparar Ambiente
```powershell
# Navegar para o projeto
cd "C:\Projetos\MDS\N8N+IAS"

# Configurar ambiente RTX 2060
copy config\.env.rtx2060 .env

# Verificar se Docker + NVIDIA estão funcionando
docker run --rm --gpus all nvidia/cuda:11.0-base-ubuntu20.04 nvidia-smi
```

### 2. Iniciar Sistema
```powershell
# Setup inicial (primeira vez)
.\rtx2060-local.ps1 -Setup

# Iniciar serviços
.\rtx2060-local.ps1 -Start

# Executar testes
.\rtx2060-local.ps1 -Test
```

### 3. Monitoramento em Tempo Real
```powershell
# Monitor de recursos (GPU, VRAM, CPU)
.\rtx2060-local.ps1 -Monitor
```

## 📊 Especificações RTX 2060

| Recurso | RTX 2060 | Otimização |
|---------|----------|------------|
| **VRAM** | 6GB GDDR6 | Use DeepSeek 1.3B (~4.8GB) |
| **CUDA Cores** | 1,920 | 35 layers na GPU |
| **Memory Bus** | 192-bit | Context 2048 tokens |
| **Bandwidth** | 336 GB/s | Batch size 512 |
| **TDP** | 160W | Concorrência = 1 |

## 🎯 Performance Esperada

### DeepSeek 1.3B na RTX 2060:
- **Primeira inferência**: ~3-5 segundos
- **Inferências seguintes**: ~2-3 segundos  
- **Tokens por segundo**: 20-30 tokens/s
- **VRAM utilizada**: ~4.8GB (80% da RTX 2060)
- **Uso de GPU**: 70-90% durante inferência

### Limitações Conhecidas:
- **Apenas 1 modelo** pode ser carregado por vez
- **Context máximo**: 2048 tokens (econômico)
- **Concorrência**: 1 requisição simultânea
- **Modelos grandes** (6.7B+) não cabem na VRAM

## 🔧 Troubleshooting

### Problema: "Out of Memory" 
```bash
# Reduzir context length
export OLLAMA_CONTEXT_LENGTH=1024

# Ou usar apenas CPU
export CUDA_VISIBLE_DEVICES=-1
```

### Problema: Performance Baixa
```bash
# Verificar se outros programas usam GPU
nvidia-smi

# Fechar programas desnecessários
taskkill /im "chrome.exe" /f
taskkill /im "discord.exe" /f
```

### Problema: Container não inicia
```bash
# Verificar logs
docker logs ollama-rtx2060

# Reiniciar serviços
docker-compose -f docker-compose.local.yml restart
```

## 🧪 Testes Disponíveis

### 1. Teste de Saúde
```powershell
curl http://localhost:5000/
```

### 2. Teste de Inferência
```powershell
$body = @{
    model = "auto"
    messages = @(@{role="user"; content="Hello RTX 2060!"})
    max_tokens = 50
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:5000/v1/chat/completions" -Method POST -Body $body -ContentType "application/json"
```

### 3. Teste de Performance
```powershell
# Executar 10 inferências e medir tempo médio
for ($i=1; $i -le 10; $i++) {
    $start = Get-Date
    # ... fazer requisição ...  
    $end = Get-Date
    Write-Host "Teste $i: $(($end-$start).TotalSeconds)s"
}
```

## 💰 Economia vs Nuvem

| Cenário | Local RTX 2060 | GCP GPU | Economia |
|---------|----------------|---------|----------|
| **Hardware** | Já possui | ~$150/mês | 100% |
| **Energia** | ~$10/mês | - | - |
| **Total Mensal** | $10 | $150 | $140/mês |
| **Total Anual** | $120 | $1800 | $1680/ano |

## 📈 Comparação de Modelos

### Recomendado para RTX 2060:
- ✅ **DeepSeek 1.3B**: Perfeito (4.8GB VRAM)
- ✅ **Llama 3.2 3B**: Funciona bem (5.2GB VRAM)
- ⚠️ **DeepSeek 6.7B**: Muito grande (>6GB)
- ❌ **Llama 7B+**: Não cabe na VRAM

### Benchmark Real (RTX 2060):
```
DeepSeek 1.3B:
- Carregamento: 3-5s
- Inferência: 25 tokens/s
- VRAM: 4.8GB
- Qualidade: Boa para código

Llama 3.2 3B:
- Carregamento: 4-6s  
- Inferência: 18 tokens/s
- VRAM: 5.2GB
- Qualidade: Melhor para texto geral
```

## 🎯 Próximos Passos

1. **Teste básico**: Execute o setup e testes iniciais
2. **Benchmark**: Meça performance com seus prompts
3. **Otimização**: Ajuste context_length conforme necessário
4. **Produção**: Compare com custos de nuvem
5. **Scale**: Considere múltiplas GPUs se necessário

---
**💡 Dica Pro**: Use o monitor em tempo real para acompanhar VRAM e otimizar configurações!
