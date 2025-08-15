import requests
import json

print("🎯 TESTE FINAL - Configuração IDEAL para Postman")

url = "http://localhost:5000/v1/chat/completions"
payload = {
    "model": "mistral",
    "messages": [
        {
            "role": "system",
            "content": "Você é Yasmin, analista financeira sênior brasileira. SEMPRE responda em português brasileiro. Seja precisa e objetiva."
        },
        {
            "role": "user",
            "content": "TechSolutions: Receita R$ 2,45M, Custos R$ 1,47M, Margem 40%, EBITDA R$ 490k, Churn 3,2%, 85 clientes. Dê 3 insights com recomendações específicas em português."
        }
    ],
    "max_tokens": 350,
    "temperature": 0.7
}

print("📋 Payload sendo enviado:")
print(json.dumps(payload, indent=2, ensure_ascii=False))
print("\n" + "="*50)

try:
    response = requests.post(url, json=payload, timeout=120)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ RESPOSTA COMPLETA:")
        print(result['choices'][0]['message']['content'])
        
        if 'usage' in result:
            tokens_used = result['usage']['completion_tokens']
            tokens_limit = payload['max_tokens']
            print(f"\n📊 Tokens: {tokens_used}/{tokens_limit} ({tokens_used/tokens_limit*100:.1f}%)")
            
            if tokens_used >= tokens_limit * 0.95:
                print("⚠️  ATENÇÃO: Resposta pode estar cortada - aumente max_tokens")
            else:
                print("✅ Resposta completa - configuração ideal!")
                
    else:
        print(f"❌ Erro HTTP {response.status_code}: {response.text}")
except Exception as e:
    print(f"❌ Erro: {e}")

print(f"\n🎯 Use essa configuração no Postman!")
