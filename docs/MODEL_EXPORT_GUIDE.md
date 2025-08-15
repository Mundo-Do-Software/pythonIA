# 📦 Guia de Exportação e Uso do Modelo Fine-Tuned

## ✅ Modelos Exportados com Sucesso!

### 📂 Arquivos Disponíveis em `exported_models/`:

#### 1. **Pickle Format** (`fine_tuned_model_pickle_*.pkl`)
- **Uso**: Integração Python padrão
- **Tamanho**: ~22 KB
- **Como usar**:
```python
import pickle
from scripts.real_fine_tuning import SimplifiedFineTuner

# Carregar modelo
tuner = SimplifiedFineTuner()
tuner.load_model('exported_models/fine_tuned_model_pickle_*.pkl')

# Fazer predição
results = tuner.predict("Como posso ajudar?", top_k=3)
print(results[0]['response'])
```

#### 2. **Joblib Format** (`fine_tuned_model_joblib_*.joblib`)
- **Uso**: Formato mais eficiente para scikit-learn
- **Tamanho**: ~23 KB
- **Como usar**:
```python
import joblib

# Carregar modelo
model_data = joblib.load('exported_models/fine_tuned_model_joblib_*.joblib')

# Reconstruir tuner
tuner = SimplifiedFineTuner()
tuner.vectorizer = model_data['vectorizer']
tuner.domain_models = model_data['domain_models']
tuner.is_trained = True

# Usar
results = tuner.predict("Sua pergunta")
```

#### 3. **Standalone Predictor** (`standalone_predictor_*.py`)
- **Uso**: Script Python independente
- **Tamanho**: ~4 KB
- **Como usar**:
```bash
# Via linha de comando
python exported_models/standalone_predictor_*.py "Como resolver problema?"

# Como módulo Python
from exported_models.standalone_predictor import predict
result = predict("Sua pergunta")
```

#### 4. **Metadados** (`model_metadata_*.json`)
- **Uso**: Informações detalhadas do modelo
- **Conteúdo**: 
  - Resumo do treinamento
  - Domínios especializados
  - Instruções de uso
  - Exemplos de integração

#### 5. **Pacote Completo** (`fine_tuned_model_package_*.zip`)
- **Uso**: Pacote completo para distribuição
- **Tamanho**: ~13 KB
- **Conteúdo**:
  - Modelo treinado
  - Scripts necessários
  - README.md
  - requirements.txt
  - Metadados

## 🚀 Formas de Usar o Modelo Exportado

### **1. Integração em Projeto Existente**
```python
# Adicionar ao seu projeto
from pathlib import Path
import sys
sys.path.append('caminho/para/scripts')

from real_fine_tuning import SimplifiedFineTuner

class MeuAssistente:
    def __init__(self):
        self.tuner = SimplifiedFineTuner()
        self.tuner.load_model('exported_models/modelo.pkl')
    
    def responder(self, pergunta):
        results = self.tuner.predict(pergunta)
        return results[0]['response'] if results else "Não entendi"

# Usar
assistente = MeuAssistente()
resposta = assistente.responder("Como cancelar pedido?")
```

### **2. API REST com Flask**
```python
from flask import Flask, request, jsonify
from real_fine_tuning import SimplifiedFineTuner

app = Flask(__name__)
tuner = SimplifiedFineTuner()
tuner.load_model('exported_models/modelo.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    query = data.get('query', '')
    
    results = tuner.predict(query, top_k=3)
    
    return jsonify({
        'query': query,
        'results': results
    })

app.run(port=8000)
```

### **3. Chatbot com Streamlit**
```python
import streamlit as st
from real_fine_tuning import SimplifiedFineTuner

@st.cache_resource
def load_model():
    tuner = SimplifiedFineTuner()
    tuner.load_model('exported_models/modelo.pkl')
    return tuner

st.title("🤖 Meu Assistente Fine-Tuned")

tuner = load_model()
query = st.text_input("Faça sua pergunta:")

if query:
    results = tuner.predict(query)
    
    for i, result in enumerate(results[:3]):
        st.write(f"**{result['domain'].title()}** ({result['confidence']*100:.1f}%)")
        st.write(result['response'])
        st.write("---")
```

### **4. Integração com a API Existente**
```python
# Adicionar ao seu simple_llm_server.py
from real_fine_tuning import SimplifiedFineTuner

class LLMServer:
    def __init__(self):
        # ... código existente ...
        
        # Carregar modelo fine-tuned
        self.fine_tuned_model = SimplifiedFineTuner()
        self.fine_tuned_model.load_model('exported_models/modelo.pkl')
    
    async def get_response(self, query):
        # 1. Tentar cache semântico (existente)
        cached = await self.check_cache(query)
        if cached:
            return cached
        
        # 2. Tentar modelo fine-tuned
        ft_results = self.fine_tuned_model.predict(query)
        if ft_results and ft_results[0]['confidence'] > 0.7:
            return ft_results[0]['response']
        
        # 3. Fallback para LLM (Ollama)
        return await self.call_ollama(query)
```

## 🎯 Casos de Uso Práticos

### **Para E-commerce**
```python
# Carregar modelo especializado em e-commerce
ecommerce_bot = SimplifiedFineTuner()
ecommerce_bot.load_model('modelo_ecommerce.pkl')

# Usar em atendimento
pergunta = "Como cancelar meu pedido?"
resposta = ecommerce_bot.predict(pergunta)[0]['response']
# Retorna: "Para cancelar: 1) Acesse Meus Pedidos, 2) Clique em Cancelar..."
```

### **Para Suporte Técnico**
```python
# Suporte especializado
suporte_bot = SimplifiedFineTuner()
suporte_bot.load_model('modelo_suporte.pkl')

pergunta = "Sistema travou, o que fazer?"
resposta = suporte_bot.predict(pergunta)[0]['response']
# Retorna resposta técnica específica
```

### **Para Consultoria/Negócios**
```python
# Consultor virtual
consultor_bot = SimplifiedFineTuner()
consultor_bot.load_model('modelo_consultoria.pkl')

pergunta = "Quanto custa uma consultoria?"
resposta = consultor_bot.predict(pergunta)[0]['response']
# Retorna informações sobre preços e pacotes
```

## 📋 Requisitos de Sistema

### **Dependências Python**
```txt
scikit-learn>=1.0.0
numpy>=1.20.0
joblib>=1.0.0
pickle (built-in)
```

### **Instalação**
```bash
pip install scikit-learn numpy joblib
```

### **Recursos de Sistema**
- **RAM**: ~50-100 MB por modelo carregado
- **Disco**: ~20-30 KB por modelo
- **CPU**: Qualquer (não precisa GPU)
- **Python**: 3.7+

## 🚀 Vantagens do Modelo Exportado

✅ **Portável** - Funciona em qualquer sistema Python  
✅ **Leve** - Apenas ~20 KB por modelo  
✅ **Rápido** - Predições em ~50-100ms  
✅ **Independente** - Não precisa do projeto original  
✅ **Flexível** - Múltiplos formatos de uso  
✅ **Especializado** - Treinado com seus dados específicos  

## 💡 Próximos Passos

1. **Testar modelo exportado** em ambiente de produção
2. **Integrar com sistema existente** usando os exemplos acima
3. **Monitorar performance** em casos reais
4. **Retreinar periodicamente** com novos dados
5. **Criar modelos especializados** para diferentes domínios

---

**🎉 Seu modelo fine-tuned está pronto para uso em produção! 🚀**
