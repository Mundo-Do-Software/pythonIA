import requests
import json

print("📊 Testando análise financeira COMPLETA...")

url = "http://localhost:5000/v1/chat/completions"
payload = {
    "model": "mistral",
    "messages": [
        {
            "role": "system",
            "content": "Você é Yasmin, analista financeira sênior. Seja detalhada e objetiva."
        },
        {
            "role": "user",
            "content": "Empresa TechSolutions:\n- Receita: R$ 2,45M\n- Custos: R$ 1,47M\n- Margem Bruta: 40%\n- EBITDA: R$ 490k\n- Churn: 3,2%\n- 85 clientes\n\nAnalise e dê 3 insights específicos com recomendações."
        }
    ],
    "max_tokens": 300,
    "temperature": 0.7
}

try:
    response = requests.post(url, json=payload, timeout=150)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Resposta COMPLETA:\n{result['choices'][0]['message']['content']}")
        
        # Vamos ver quantos tokens foram usados
        if 'usage' in result:
            print(f"\n📊 Tokens usados: {result['usage']}")
    else:
        print(f"❌ Erro HTTP {response.status_code}: {response.text}")
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n🎯 Teste completo finalizado!")
