import requests

# Teste super simples
payload = {
    "model": "mistral",
    "messages": [
        {
            "role": "user",
            "content": "Analise: Receita R$ 100.000, Custo R$ 70.000. Margem 30%. É bom?"
        }
    ],
    "temperature": 0.5,
    "max_tokens": 80
}

import requests
import json

print("🧪 Teste super simples...")

url = "http://localhost:5000/v1/chat/completions"
payload = {
    "model": "mistral",
    "messages": [
        {"role": "user", "content": "Olá! Responda brevemente."}
    ],
    "max_tokens": 50,
    "temperature": 0.5
}

try:
    response = requests.post(url, json=payload, timeout=120)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Resposta: {result['choices'][0]['message']['content']}")
    else:
        print(f"❌ Erro HTTP {response.status_code}: {response.text}")
except Exception as e:
    print(f"❌ Erro: {e}")

print("🎯 Teste concluído!")
response = requests.post('http://localhost:5000/v1/chat/completions', json=payload)

if response.status_code == 200:
    result = response.json()
    print('✅ Resposta:', result['choices'][0]['message']['content'])
else:
    print('❌ Erro:', response.status_code)
