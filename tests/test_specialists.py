import requests
import json

BASE_URL = "http://localhost:5000"

def test_specialists():
    """Testa os especialistas YASMIN e RICARDO"""
    
    print("🧪 TESTE DOS ESPECIALISTAS")
    print("=" * 50)
    
    # TESTE 1: YASMIN - Análise Financeira
    print("1️⃣ YASMIN - ANÁLISE FINANCEIRA:")
    yasmin_request = {
        "model": "auto",
        "messages": [
            {"role": "system", "content": "Você é YASMIN, uma especialista em análise financeira e consultoria empresarial. Seja analítica, direta e use insights profissionais. Limite: 600 tokens."},
            {"role": "user", "content": "Analisar estes KPIs: Receita R$ 5M, Margem 35%, EBITDA R$ 1.2M, Churn 8%. O que diz sobre a saúde financeira?"}
        ],
        "max_tokens": 600,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(f"{BASE_URL}/v1/chat/completions", json=yasmin_request, timeout=60)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Modelo: {data.get('model', 'N/A')}")
            print(f"   📊 Resposta: {data['choices'][0]['message']['content'][:200]}...")
        else:
            print(f"   ❌ Erro HTTP: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print()
    
    # TESTE 2: RICARDO - Diagnóstico Mecânico
    print("2️⃣ RICARDO - DIAGNÓSTICO MECÂNICO:")
    ricardo_request = {
        "model": "auto", 
        "messages": [
            {"role": "system", "content": "Você é RICARDO, um mecânico especialista em motocicletas com 15 anos de experiência. Seja prático, direto e use linguagem técnica apropriada. Limite: 300 tokens."},
            {"role": "user", "content": "Minha moto Honda CB600 está com ruído estranho no motor quando acelero. O que pode ser?"}
        ],
        "max_tokens": 300,
        "temperature": 0.6
    }
    
    try:
        response = requests.post(f"{BASE_URL}/v1/chat/completions", json=ricardo_request, timeout=60)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Modelo: {data.get('model', 'N/A')}")
            print(f"   🔧 Resposta: {data['choices'][0]['message']['content'][:200]}...")
        else:
            print(f"   ❌ Erro HTTP: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print()
    
    # TESTE 3: Pergunta Simples (deveria usar Llama 3.2)
    print("3️⃣ PERGUNTA SIMPLES (LLAMA 3.2):")
    simple_request = {
        "model": "auto",
        "messages": [{"role": "user", "content": "Oi, tudo bem?"}],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(f"{BASE_URL}/v1/chat/completions", json=simple_request, timeout=60)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Modelo: {data.get('model', 'N/A')}")
            print(f"   💬 Resposta: {data['choices'][0]['message']['content']}")
        else:
            print(f"   ❌ Erro HTTP: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")

if __name__ == "__main__":
    test_specialists()
