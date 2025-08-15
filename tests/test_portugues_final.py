import requests
import json

print("🇧🇷 TESTE PORTUGUÊS BRASILEIRO - Configuração FINAL")

url = "http://localhost:5000/v1/chat/completions"
payload = {
    "model": "mistral",
    "messages": [
        {
            "role": "system",
            "content": "Você é YASMIN, analista financeira brasileira. SEMPRE responda em português brasileiro. Seja objetiva e concisa."
        },
        {
            "role": "user",
            "content": "TechSolutions: Receita R$ 2,45M, Custos R$ 1,47M, Margem 40%, EBITDA R$ 490k, Churn 3,2%, 85 clientes. Dê 3 insights curtos com 1 recomendação cada."
        }
    ],
    "max_tokens": 600,
    "temperature": 0.6
}

print("📋 Payload para Postman:")
print(json.dumps(payload, indent=2, ensure_ascii=False))
print("\n" + "="*60)

try:
    response = requests.post(url, json=payload, timeout=150)
    if response.status_code == 200:
        result = response.json()
        print("✅ RESPOSTA DA YASMIN:")
        print("-" * 40)
        print(result['choices'][0]['message']['content'])
        print("-" * 40)
        
        if 'usage' in result:
            tokens_used = result['usage']['completion_tokens']
            tokens_limit = payload['max_tokens']
            percentage = tokens_used/tokens_limit*100
            print(f"\n📊 Análise de Tokens:")
            print(f"   • Usados: {tokens_used}")
            print(f"   • Limite: {tokens_limit}")
            print(f"   • Percentual: {percentage:.1f}%")
            
            if tokens_used >= tokens_limit * 0.90:
                print("⚠️ ATENÇÃO: Resposta pode estar cortada - considere aumentar max_tokens")
            else:
                print("✅ Resposta completa - configuração aprovada!")
                
    else:
        print(f"❌ Erro HTTP {response.status_code}: {response.text}")
except Exception as e:
    print(f"❌ Erro: {e}")

print(f"\n🎯 Esta é a configuração FINAL para usar no Postman!")
print("📝 Copy/paste o JSON acima diretamente no Body do Postman")
