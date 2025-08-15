# 📊 Guia de Testes Financeiros - Postman

## ⚡ IMPORTANTE - Token Limits
> **ATENÇÃO**: Para respostas completas, use `max_tokens` entre 200-250
> **Recomendação**: 200 tokens = respostas concisas e completas
> **Máximo testado**: 300 tokens (pode cortar no final)

## 🚀 Configuração Básica Postman:
- **Method**: POST
- **URL**: `http://localhost:5000/v1/chat/completions`
- **Headers**: 
  - `Content-Type: application/json`
  - `Authorization: Bearer dummy-key` (opcional)

---

## 💼 Exemplo 1: Análise KPI Rápida (200 tokens - IDEAL)

```json
{
  "model": "mistral",
  "messages": [
    {
      "role": "system",
      "content": "Você é Yasmin, analista financeira. Responda objetivamente."
    },
    {
      "role": "user",
      "content": "Dados: Receita R$ 2,45M, Custos R$ 1,47M, Margem 40%, EBITDA R$ 490k, Churn 3,2%. Liste 3 insights específicos."
    }
  ],
  "temperature": 0.7,
  "max_tokens": 200,
  "stream": false
}
```

---

## 📈 Exemplo 2: Análise de Tendências (220 tokens)

```json
{
  "model": "mistral",
  "messages": [
    {
      "role": "system",
      "content": "Você é especialista em tendências financeiras."
    },
    {
      "role": "user",
      "content": "Empresa cresceu 8,5% no mês. Margem bruta caiu de 42% para 40%. CAC subiu 15%. LTV manteve R$ 12.800. Analise essas tendências e sugira 2 ações."
    }
  ],
  "temperature": 0.8,
  "max_tokens": 220,
  "stream": false
}
```

---

## 💡 Exemplo 3: Recomendações Estratégicas (180 tokens)

```json
{
  "model": "mistral",
  "messages": [
    {
      "role": "system",
      "content": "Você é consultor estratégico financeiro."
    },
    {
      "role": "user",
      "content": "Software B2B, 85 clientes, churn 3,2%, CAC R$ 850, LTV R$ 12.800. Margem operacional: 22%. Sugerir 2 melhorias prioritárias."
    }
  ],
  "temperature": 0.6,
  "max_tokens": 180,
  "stream": false
}
```

---

## 🎯 Exemplo 4: Comparação Setorial (100 tokens)

```json
{
  "model": "mistral",
  "messages": [
    {
      "role": "user",
      "content": "Margem bruta 40%, churn 3,2%, CAC/LTV ratio 1:15. Como está vs mercado SaaS B2B?"
    }
  ],
  "temperature": 0.5,
  "max_tokens": 100,
  "stream": false
}
```

---

## 🔍 Exemplo 5: Diagnóstico Rápido (80 tokens)

```json
{
  "model": "mistral",
  "messages": [
    {
      "role": "user",
      "content": "EBITDA R$ 490k, receita R$ 2,45M, 85 clientes. Principal problema?"
    }
  ],
  "temperature": 0.3,
  "max_tokens": 80,
  "stream": false
}
```

---

## ✅ Checklist de Testes:

1. **Teste Básico** (80 tokens): Confirmar API funcionando
2. **Teste Médio** (150 tokens): Análise completa sem timeout
3. **Teste Complexo** (200 tokens): Máximo recomendado
4. **Streaming Test**: Adicionar `"stream": true` se necessário

## 🚨 Troubleshooting:

- **Timeout**: Reduza `max_tokens` para 100-120
- **Resposta incompleta**: Simplifique o prompt
- **Erro 500**: Verifique se containers estão rodando
- **Sem GPU**: Resposta mais lenta, mas funcional

## 📋 Métricas para Testar:
- ROI, ROAS, CAC, LTV
- Margem Bruta/Líquida
- Churn Rate, NPS
- EBITDA, FCO
- Conversão, Retenção

---
*Última atualização: Dezembro 2024*
*Otimizado para RTX 2060 + Mistral 7B*
