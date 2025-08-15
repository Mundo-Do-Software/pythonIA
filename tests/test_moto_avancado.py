import requests
import json

print("🏍️ TESTE AVANÇADO - Diagnóstico Complexo de Motocicleta")

url = "http://localhost:5000/v1/chat/completions"
payload = {
    "model": "mistral",
    "messages": [
        {
            "role": "system",
            "content": "Você é RICARDO, mecânico especialista em motocicletas com 20 anos de experiência. SEMPRE responda em português brasileiro. Seja técnico mas didático, explicando o problema e a solução passo a passo."
        },
        {
            "role": "user",
            "content": "Honda CB600F 2010 com 85.000km: Motor liga mas morre após 2-3 minutos quando esquenta. Marcha lenta irregular, às vezes acelera sozinha até 3000rpm. Combustível novo, filtro de ar limpo, velas trocadas há 1 mês. Sensor de temperatura parece OK. Diagnóstico completo e solução passo a passo?"
        }
    ],
    "max_tokens": 600,
    "temperature": 0.6
}

try:
    response = requests.post(url, json=payload, timeout=150)
    if response.status_code == 200:
        result = response.json()
        print("✅ DIAGNÓSTICO COMPLETO DO RICARDO:")
        print("=" * 60)
        print(result['choices'][0]['message']['content'])
        print("=" * 60)
        
        if 'usage' in result:
            tokens_used = result['usage']['completion_tokens']
            print(f"\n📊 Tokens utilizados: {tokens_used}/600 ({tokens_used/600*100:.1f}%)")
    else:
        print(f"❌ Erro: {response.status_code} - {response.text}")
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n🔧 Modelo RICARDO pronto para uso profissional!")
