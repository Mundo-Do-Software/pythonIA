import requests
import json

print("🤖 TESTE DE SELEÇÃO AUTOMÁTICA DE MODELOS")

url = "http://localhost:5000/v1/chat/completions"

# Teste 1: Pergunta simples (deve usar modelo leve quando disponível)
print("\n1️⃣ TESTE SIMPLES:")
payload_simple = {
    "model": "auto",
    "messages": [
        {"role": "user", "content": "Olá! Como você está?"}
    ],
    "max_tokens": 100,
    "temperature": 0.5
}

try:
    response = requests.post(url, json=payload_simple, timeout=120)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Modelo usado: {result['model']}")
        print(f"📝 Resposta: {result['choices'][0]['message']['content']}")
    else:
        print(f"❌ Erro: {response.status_code}")
except Exception as e:
    print(f"❌ Erro: {e}")

# Teste 2: Análise financeira (deve usar Mistral)
print("\n2️⃣ TESTE COMPLEXO (FINANCEIRO):")
payload_complex = {
    "model": "auto",
    "messages": [
        {"role": "user", "content": "Analise os KPIs: Receita R$ 2M, Margem 40%, EBITDA R$ 400k. Dê insights estratégicos."}
    ],
    "max_tokens": 300,
    "temperature": 0.6
}

try:
    response = requests.post(url, json=payload_complex, timeout=120)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Modelo usado: {result['model']}")
        print(f"📝 Resposta: {result['choices'][0]['message']['content'][:200]}...")
    else:
        print(f"❌ Erro: {response.status_code}")
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n🎯 Teste de seleção automática concluído!")
