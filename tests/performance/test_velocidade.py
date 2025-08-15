import requests
import json
import time

print("⚡ TESTE DE VELOCIDADE - Configuração Otimizada")

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

print("🚀 Enviando requisição...")
start_time = time.time()

try:
    response = requests.post(url, json=payload, timeout=120)
    end_time = time.time()
    duration = end_time - start_time
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ SUCESSO em {duration:.2f} segundos!")
        print("-" * 50)
        print(result['choices'][0]['message']['content'])
        print("-" * 50)
        
        if 'usage' in result:
            tokens_used = result['usage']['completion_tokens']
            print(f"📊 Tokens: {tokens_used}/600 ({tokens_used/600*100:.1f}%)")
            print(f"⚡ Velocidade: {tokens_used/duration:.1f} tokens/segundo")
            
    else:
        print(f"❌ Erro HTTP {response.status_code}: {response.text}")
except Exception as e:
    print(f"❌ Erro: {e}")

print(f"\n🎯 CONFIGURAÇÃO FINAL APROVADA PARA POSTMAN!")
print("📝 JSON pronto para copiar e colar:")
