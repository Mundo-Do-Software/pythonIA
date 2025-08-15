import requests
import json

print("📊 Testando análise financeira básica...")

url = "http://localhost:5000/v1/chat/completions"
payload = {
    "model": "mistral",
    "messages": [
        {
            "role": "system",
            "content": "Você é Yasmin, analista financeira. Responda objetivamente."
        },
        {
            "role": "user",
            "content": "Dados: Receita R$ 2,45M, Custos R$ 1,47M, Margem 40%, EBITDA R$ 490k, Churn 3,2%. Liste 2 insights curtos."
        }
    ],
    "max_tokens": 200,
    "temperature": 0.7
}

try:
    response = requests.post(url, json=payload, timeout=120)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Resposta:\n{result['choices'][0]['message']['content']}")
    else:
        print(f"❌ Erro HTTP {response.status_code}: {response.text}")
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n🎯 Teste financeiro concluído!")
