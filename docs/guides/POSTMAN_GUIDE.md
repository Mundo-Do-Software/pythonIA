# 📡 Guia Postman - API de Chat

## 🚀 Configuração Básica

### **URL Base**: `http://localhost:5000`

### **Headers Obrigatórios**:
```
Content-Type: application/json
```

---

## 📋 **Endpoints Disponíveis**

### 1. **Health Check** 
- **GET** `http://localhost:5000/`
- **Resposta**:
```json
{
  "status": "running",
  "backend": "connected",
  "model": "mistral",
  "api_version": "1.0.0"
}
```

### 2. **Listar Modelos**
- **GET** `http://localhost:5000/v1/models`
- **Resposta**:
```json
{
  "object": "list",
  "data": [
    {
      "id": "mistral",
      "object": "model",
      "created": 1753931366,
      "owned_by": "local"
    }
  ]
}
```

### 3. **Chat Completions** (Principal)
- **POST** `http://localhost:5000/v1/chat/completions`

---

## 💬 **Exemplos de Body (JSON)**

### **Exemplo 1: Conversa Simples**
```json
{
  "model": "mistral",
  "messages": [
    {
      "role": "user",
      "content": "Olá! Como você está?"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 150
}
```

### **Exemplo 2: Com Context System**
```json
{
  "model": "mistral",
  "messages": [
    {
      "role": "system",
      "content": "Você é um assistente especializado em tecnologia. Responda de forma técnica e precisa."
    },
    {
      "role": "user",
      "content": "Explique o que é Docker em termos técnicos."
    }
  ],
  "temperature": 0.7,
  "max_tokens": 300
}
```

### **Exemplo 3: Conversa Contínua**
```json
{
  "model": "mistral",
  "messages": [
    {
      "role": "user",
      "content": "Qual é a capital do Brasil?"
    },
    {
      "role": "assistant", 
      "content": "A capital do Brasil é Brasília."
    },
    {
      "role": "user",
      "content": "Quantos habitantes tem essa cidade?"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 200
}
```

### **Exemplo 4: Especialista Financeiro (Como na imagem)**
```json
{
  "model": "mistral",
  "messages": [
    {
      "role": "system",
      "content": "Você é uma especialista financeira chamada Yasmin. Sua função é controlar a saúde financeira da empresa Mundo do Software. Responda em português brasileiro, de forma objetiva e sem inventar informações."
    },
    {
      "role": "user",
      "content": "Nosso faturamento mensal é R$ 10.000,00. Temos um cliente apenas e estamos no regime tributário do simples nacional, sou o único sócio e não tenho colaboradores. Sabendo disso, prepare um planejamento financeiro para esse negócio, divida todas as despesas e mostre quanto podemos usar para benefício próprio, lucro e pró-labore."
    }
  ],
  "temperature": 0.7,
  "max_tokens": 500,
  "stream": false
}
```

---

## ⚙️ **Parâmetros Opcionais**

```json
{
  "model": "mistral",
  "messages": [...],
  "temperature": 0.7,      // 0.0 = determinístico, 1.0 = criativo
  "max_tokens": 300,       // Máximo de tokens na resposta
  "top_p": 0.9,           // Nucleus sampling
  "top_k": 40,            // Top-k sampling
  "stream": false         // Se true, resposta em streaming
}
```

---

## 📨 **Resposta Esperada**

```json
{
  "id": "chatcmpl-uuid-aqui",
  "object": "chat.completion",
  "created": 1753931366,
  "model": "mistral",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Resposta da IA aqui..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 50,
    "total_tokens": 75
  }
}
```

---

## 🚨 **Possíveis Erros**

### **Erro 404**: Modelo não encontrado
```json
{
  "choices": [
    {
      "message": {
        "content": "Erro na chamada do Ollama: 404"
      }
    }
  ]
}
```
**Solução**: Execute `python setup_model.py`

### **Erro 500**: Servidor interno
```json
{
  "detail": "Descrição do erro"
}
```

### **Erro de Parse**: Body malformado
```json
{
  "detail": "There was an error parsing the body"
}
```

---

## 🧪 **Testando no Postman**

1. **Abra Postman**
2. **Crie nova requisição POST**
3. **URL**: `http://localhost:5000/v1/chat/completions`
4. **Headers**: Adicione `Content-Type: application/json`
5. **Body**: Selecione "raw" + "JSON" e cole um dos exemplos
6. **Clique Send**

### **Status de Sucesso**: `200 OK`
### **Tempo esperado**: 1-5 segundos
