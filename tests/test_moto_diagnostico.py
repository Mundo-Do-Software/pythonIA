import requests
import json

print("🏍️ DIAGNÓSTICO DE MOTOCICLETAS - Modelo RICARDO")

url = "http://localhost:5000/v1/chat/completions"
payload = {
    "model": "mistral",
    "messages": [
        {
            "role": "system",
            "content": "Você é RICARDO, mecânico especialista em motocicletas. SEMPRE responda em português brasileiro. Seja técnico mas didático."
        },
        {
            "role": "user",
            "content": "Honda CB600F 2010: Motor morre após 2-3 min quando esquenta, marcha lenta irregular, às vezes acelera sozinha. Combustível novo, filtro limpo. Diagnóstico e solução passo a passo?"
        }
    ],
    "max_tokens": 600,
    "temperature": 0.6
}

try:
    response = requests.post(url, json=payload, timeout=150)
    if response.status_code == 200:
        result = response.json()
        print("✅ DIAGNÓSTICO DO RICARDO:")
        print("-" * 50)
        print(result['choices'][0]['message']['content'])
        print("-" * 50)
        
        if 'usage' in result:
            tokens_used = result['usage']['completion_tokens']
            print(f"📊 Tokens: {tokens_used}/600 ({tokens_used/600*100:.1f}%)")
                
    else:
        print(f"❌ Erro HTTP {response.status_code}: {response.text}")
except Exception as e:
    print(f"❌ Erro: {e}")

print(f"\n🔧 Modelo pronto para diagnóstico de motocicletas!")
