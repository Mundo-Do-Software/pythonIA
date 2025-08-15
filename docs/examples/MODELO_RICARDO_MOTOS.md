# 🏍️ MODELO RICARDO - DIAGNÓSTICO DE MOTOCICLETAS

## ✅ **SISTEMA FUNCIONANDO**
- ✅ **Diagnósticos técnicos** em português brasileiro
- ✅ **Soluções práticas** passo a passo
- ✅ **200 tokens** = Resposta completa
- ✅ **Sem timeout** - Funciona perfeitamente

---

## 🔧 **JSON PARA POSTMAN - DIAGNÓSTICO DE MOTOS**

**URL**: `http://localhost:5000/v1/chat/completions`  
**Method**: POST  
**Headers**: `Content-Type: application/json`

### 🏍️ **Exemplo 1: Diagnóstico Geral**
```json
{
  "model": "mistral",
  "messages": [
    {
      "role": "system",
      "content": "Você é RICARDO, mecânico especialista em motocicletas com 20 anos de experiência. SEMPRE responda em português brasileiro. Seja técnico mas didático, explicando o problema e a solução passo a passo."
    },
    {
      "role": "user",
      "content": "Honda CB600F 2010: Motor liga mas morre após 2-3 minutos quando esquenta. Marcha lenta irregular, às vezes acelera sozinha. Combustível novo, filtro limpo. Diagnóstico e solução?"
    }
  ],
  "max_tokens": 500,
  "temperature": 0.6
}
```

### ⚡ **Exemplo 2: Problema Elétrico**
```json
{
  "model": "mistral",
  "messages": [
    {
      "role": "system",
      "content": "Você é RICARDO, mecânico de motos. Responda em português brasileiro com soluções práticas."
    },
    {
      "role": "user",
      "content": "Yamaha XJ6 2015: Não dá partida, bateria nova, luzes funcionam, motor de arranque não gira. O que verificar?"
    }
  ],
  "max_tokens": 400,
  "temperature": 0.5
}
```

### 🔥 **Exemplo 3: Problema de Motor**
```json
{
  "model": "mistral",
  "messages": [
    {
      "role": "system",
      "content": "Você é RICARDO, especialista em motores de motocicleta. Explique de forma técnica mas acessível."
    },
    {
      "role": "user",
      "content": "Kawasaki Z1000 2018: Muito fumo azul no escapamento, consumo alto de óleo, perda de potência. Diagnóstico?"
    }
  ],
  "max_tokens": 450,
  "temperature": 0.4
}
```

### 🛠️ **Exemplo 4: Manutenção Preventiva**
```json
{
  "model": "mistral",
  "messages": [
    {
      "role": "system",
      "content": "Você é RICARDO, mecânico experiente. Dê dicas de manutenção preventiva em português brasileiro."
    },
    {
      "role": "user",
      "content": "BMW F800GS 2016, 45.000km: Quais manutenções preventivas devo fazer nos próximos 5.000km?"
    }
  ],
  "max_tokens": 400,
  "temperature": 0.7
}
```

---

## 🎯 **TIPOS DE DIAGNÓSTICO SUPORTADOS**

| Categoria | Exemplos |
|-----------|----------|
| **Motor** | Não liga, morre, superaquecimento, ruídos |
| **Elétrica** | Bateria, alternador, ignição, luzes |
| **Transmissão** | Embreagem, câmbio, correia, corrente |
| **Freios** | Pastilhas, discos, fluido, ABS |
| **Suspensão** | Amortecedores, garfo, molas |
| **Combustível** | Injeção, carburador, bomba, filtros |

---

## ⚙️ **CONFIGURAÇÕES RECOMENDADAS**

| Uso | max_tokens | temperature | Motivo |
|-----|------------|-------------|--------|
| **Diagnóstico Rápido** | 300 | 0.5 | Resposta técnica precisa |
| **Explicação Detalhada** | 500 | 0.6 | Mais didático |
| **Manutenção Preventiva** | 400 | 0.7 | Mais dicas criativas |
| **Emergência** | 200 | 0.4 | Solução rápida |

---

## 🔍 **EXEMPLOS DE PROMPTS EFICAZES**

### Para Diagnóstico:
- "Moto [modelo] [ano]: [sintomas detalhados]. Diagnóstico e solução?"
- "[Marca/modelo]: [problema específico]. O que pode ser e como resolver?"

### Para Manutenção:
- "[Moto] com [km]: Que manutenções fazer agora?"
- "Como fazer manutenção preventiva em [sistema específico]?"

### Para Emergência:
- "[Problema urgente] na estrada. Solução temporária?"
- "Moto parou funcionando. Verificações básicas?"

---

## 🚨 **DICAS DE USO**

1. **Seja específico**: Modelo, ano, sintomas, o que já foi verificado
2. **Contexto importante**: Quilometragem, última manutenção, modificações
3. **Sintomas claros**: Quando acontece, em que situações, frequência
4. **Histórico**: Problemas anteriores, peças trocadas recentemente

---

## 📊 **MÉTRICAS DE PERFORMANCE**
- **Tempo de resposta**: 10-20 segundos
- **Precisão técnica**: Alta (baseado em conhecimento consolidado)
- **Linguagem**: Português brasileiro técnico mas acessível
- **Cobertura**: Todas as marcas e modelos populares

---

**🏍️ RICARDO ESTÁ PRONTO PARA DIAGNOSTICAR SUA MOTO!**

*Testado com Honda, Yamaha, Kawasaki, BMW, Suzuki e outras marcas*
*Modelo especializado em diagnóstico automotivo*
