import requests
import json

print("🔧 TESTE SIMPLES DE MOTOCICLETAS")

url = "http://localhost:5000/v1/chat/completions"
payload = {
    "model": "mistral",
    "messages": [
        {
            "role": "system",
            "content": "Você é Ricardo, mecânico de motos. Responda em português."
        },
        {
            "role": "user",
            "content": "Moto não liga. O que pode ser?"
        }
    ],
    "max_tokens": 200,
    "temperature": 0.6
}

try:
    response = requests.post(url, json=payload, timeout=150)
    if response.status_code == 200:
        result = response.json()
        print("✅ RESPOSTA:")
        print(result['choices'][0]['message']['content'])
    else:
        print(f"❌ Erro: {response.status_code} - {response.text}")
except Exception as e:
    print(f"❌ Erro: {e}")

print("🔚 Teste concluído")
