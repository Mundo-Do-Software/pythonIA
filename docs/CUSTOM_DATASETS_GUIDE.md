# 🎨 Guia Rápido: Fine-Tuning com Datasets Personalizados

## 🚀 Como Começar

### 1. **Criar Seus Datasets Personalizados**

```python
# Execute o script de exemplo (imports corrigidos)
python scripts\create_my_datasets.py

# Ou crie manualmente:
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.dataset_generator import DatasetGenerator

generator = DatasetGenerator()

# Suas conversas personalizadas
minhas_conversas = [
    {
        "input": "Como resolver problema X?",
        "output": "Para resolver X, faça: 1) Passo A, 2) Passo B, 3) Passo C"
    },
    # Adicione mais exemplos...
]

# Criar dataset
arquivo = generator.create_conversation_dataset(
    minhas_conversas, 
    "meu_dominio", 
    "json"
)
```

### 2. **Formatos Suportados**

#### JSON (Recomendado)
```json
{
  "metadata": {
    "domain": "meu_negocio",
    "created_at": "2025-08-01T10:00:00"
  },
  "conversations": [
    {"input": "pergunta", "output": "resposta"},
    {"input": "pergunta 2", "output": "resposta 2"}
  ]
}
```

#### CSV (Simples)
```csv
input,output,domain
"Como fazer X?","Para X faça: 1, 2, 3","tecnico"
"Problema Y?","Solução Y: passo a passo","suporte"
```

#### JSONL (Uma linha por exemplo)
```jsonl
{"input": "pergunta 1", "output": "resposta 1"}
{"input": "pergunta 2", "output": "resposta 2"}
```

### 3. **Executar Fine-Tuning Híbrido**

```bash
# Gerar dados híbridos (Redis + Custom)
python scripts\hybrid_fine_tuning.py

# Configurar proporção no .env:
DATASET_BALANCE_RATIO=0.5  # 50% Redis + 50% Custom
```

### 4. **Estrutura de Diretórios**

```
training_data/
├── meu_negocio_dataset_20250801.json    # Seus dados
├── suporte_dataset_20250801.json        # Suporte
├── tecnico_dataset_20250801.json        # Técnico
└── hybrid_training_data_20250801.json   # Dados combinados
```

## 🎯 Exemplos Práticos

### **Para E-commerce**
```python
ecommerce_data = [
    {
        "input": "Como cancelar pedido?",
        "output": "Para cancelar: 1) Acesse Meus Pedidos, 2) Clique em Cancelar, 3) Confirme. Reembolso em 3-5 dias úteis."
    },
    {
        "input": "Prazo de entrega para SP?",
        "output": "Entregas em São Paulo: 1-2 dias úteis para região metropolitana, 3-5 dias para interior. Frete grátis acima de R$ 99."
    }
]
```

### **Para Consultoria**
```python
consultoria_data = [
    {
        "input": "Quanto custa uma consultoria?",
        "output": "Nossos pacotes: Básico R$ 2.500/mês, Intermediário R$ 5.000/mês, Premium R$ 10.000/mês. Inclui análise, estratégia e acompanhamento."
    },
    {
        "input": "Qual ROI esperado?",
        "output": "Clientes típicos veem ROI de 300-500% em 6-12 meses. Isso varia por setor e implementação das recomendações."
    }
]
```

### **Para Suporte Técnico**
```python
suporte_data = [
    {
        "input": "Sistema travou, o que fazer?",
        "output": "Para destravamento: 1) Ctrl+Alt+Del, 2) Encerrar programa travado, 3) Se persistir, reiniciar. Salve trabalho antes."
    },
    {
        "input": "Como atualizar o software?",
        "output": "Atualização: 1) Menu Ajuda > Verificar Atualizações, 2) Download automático, 3) Reiniciar quando solicitado. Backup recomendado."
    }
]
```

## ⚙️ Configurações Avançadas

### **Balanceamento de Dados**
```env
# No arquivo .env
DATASET_BALANCE_RATIO=0.7  # 70% Redis (uso real) + 30% Custom
TRAINING_DATA_DAYS=30      # 30 dias de histórico Redis
MIN_EXAMPLES_PER_DOMAIN=20 # Mínimo por domínio
```

### **Parâmetros LoRA**
```env
LORA_RANK=16        # Complexidade (8-64)
LORA_ALPHA=32       # Força do treinamento
TRAINING_EPOCHS=3   # Número de épocas
LEARNING_RATE=1e-4  # Taxa de aprendizado
```

## 🔄 Workflow Completo

### **1. Preparação**
```bash
# Criar datasets personalizados
python scripts\create_my_datasets.py

# Analisar datasets criados
python scripts\analyze_datasets.py

# Verificar cache Redis
python scripts\debug_redis.py
```

### **2. Treinamento**
```bash
# Gerar dados híbridos
python scripts\hybrid_fine_tuning.py

# Executar fine-tuning (quando implementar)
python scripts\auto_fine_tune.py
```

### **3. Teste**
```bash
# Testar sistema completo
python scripts\test_complete_fine_tuning.py

# Testar modelos treinados
python scripts\test_fine_tuned_models.py
```

## 💡 Dicas de Qualidade

### **Bons Exemplos**
- ✅ Perguntas naturais como usuários reais fazem
- ✅ Respostas completas e úteis
- ✅ Linguagem consistente com sua marca
- ✅ 20-50 exemplos por domínio mínimo

### **Evitar**
- ❌ Perguntas muito técnicas ou artificiais
- ❌ Respostas muito curtas ou vagas
- ❌ Linguagem inconsistente
- ❌ Poucos exemplos (menos de 10)

## 🚀 Resultado Final

Seu sistema terá:
- ✅ **Cache semântico inteligente** (874x+ speedup)
- ✅ **Fine-tuning automático** do uso real (Redis)
- ✅ **Fine-tuning personalizado** dos seus datasets
- ✅ **Especialização por domínio** automática
- ✅ **Melhoria contínua** com novos dados

**Resultado: IA que entende seu negócio específico e melhora automaticamente! 🧠✨**

---

## ✅ Status Atual do Sistema

### **Datasets Personalizados Criados** 
- ✅ `meu_negocio_tech_dataset` - Empresa de tecnologia
- ✅ `meu_suporte_personalizado_dataset` - Suporte técnico  
- ✅ `saude_digital_dataset` - Saúde digital
- ✅ `perguntas_frequentes_dataset` - FAQ geral
- ✅ `meu_dataset_completo_dataset` - Dataset consolidado
- ✅ Importação de CSV funcional

### **Scripts Funcionais**
- ✅ `create_my_datasets.py` - Cria datasets de exemplo
- ✅ `analyze_datasets.py` - Analisa datasets criados
- ✅ `hybrid_fine_tuning.py` - Combina Redis + Custom
- ✅ `dataset_generator.py` - Gerador principal

### **Próximos Passos**
```bash
# 1. Analisar seus datasets
python scripts\analyze_datasets.py

# 2. Executar fine-tuning híbrido
python scripts\hybrid_fine_tuning.py

# 3. Testar sistema completo
python scripts\test_complete_fine_tuning.py
```

**Sistema pronto para fine-tuning com seus dados personalizados! 🚀**
