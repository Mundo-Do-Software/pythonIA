import requests

payload = {
    "model": "mistral",
    "messages": [
        {
            "role": "system",
            "content": "Você é uma analista financeira. Analise dados e forneça insights práticos."
        },
        {
            "role": "user",
            "content": "Empresa teve:\n- Receita: R$ 500.000\n- Custos: R$ 380.000\n- Lucro: R$ 120.000\n- Margem: 24%\n\nEssa performance é boa? Dê 2 insights principais."
        }
    ],
    "temperature": 0.6,
    "max_tokens": 150
}

print('🧪 Teste financeiro simples...')
response = requests.post('http://localhost:5000/v1/chat/completions', json=payload)

if response.status_code == 200:
    result = response.json()
    analysis = result['choices'][0]['message']['content']
    print('✅ Resposta da IA:')
    print('=' * 50)
    print(analysis)
    print('=' * 50)
else:
    print(f'❌ Erro: {response.status_code}')
    print(response.text)