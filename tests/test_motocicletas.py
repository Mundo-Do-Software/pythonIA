import requests
import json

print("🏍️ TESTE DIAGNÓSTICO DE MOTOCICLETAS")

url = "http://localhost:5000/v1/chat/completions"
payload = {
    "model": "mistral",
    "messages": [
        {
            "role": "system",
            "content": "Você é RICARDO, mecânico de motos. SEMPRE responda em português brasileiro. Seja prático e didático."
        },
        {
            "role": "user",
            "content": "Honda CB600F 2010: Motor morre após 2-3 min quando esquenta, marcha lenta irregular. Diagnóstico e solução?"
        }
    ],
    "max_tokens": 600,
    "temperature": 0.6
}

print("📋 Payload para diagnóstico de motos:")
print(json.dumps(payload, indent=2, ensure_ascii=False))
print("\n" + "="*60)

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
            tokens_limit = payload['max_tokens']
            percentage = tokens_used/tokens_limit*100
            print(f"\n📊 Análise de Tokens:")
            print(f"   • Usados: {tokens_used}")
            print(f"   • Limite: {tokens_limit}")
            print(f"   • Percentual: {percentage:.1f}%")
                
    else:
        print(f"❌ Erro HTTP {response.status_code}: {response.text}")
except Exception as e:
    print(f"❌ Erro: {e}")

print(f"\n🔧 Configuração para diagnóstico de motocicletas!")
