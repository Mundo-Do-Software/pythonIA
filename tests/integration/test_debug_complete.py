#!/usr/bin/env python3
"""
Teste direto do sistema multi-modelo
"""
import requests
import json

def test_auto_selection():
    url = "http://localhost:5000/v1/chat/completions"
    
    print("🧪 TESTE DE SELEÇÃO AUTOMÁTICA")
    print("=" * 50)
    
    # Teste 1: Saudação simples (deve usar Llama 3.2)
    print("\n1️⃣ TESTE SIMPLES - Saudação:")
    payload = {
        "model": "auto",
        "messages": [
            {"role": "user", "content": "Olá! Como você está?"}
        ],
        "max_tokens": 100,
        "temperature": 0.5
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   🤖 Modelo retornado: {result['model']}")
            print(f"   📝 Resposta: {result['choices'][0]['message']['content'][:100]}...")
        else:
            print(f"   ❌ Erro HTTP: {response.status_code}")
            print(f"   📄 Resposta: {response.text}")
    except Exception as e:
        print(f"   ❌ Exceção: {e}")
    
    # Teste 2: Análise financeira (deve usar Mistral)
    print("\n2️⃣ TESTE COMPLEXO - Análise Financeira:")
    payload = {
        "model": "auto",
        "messages": [
            {"role": "user", "content": "Preciso de uma análise financeira dos KPIs de uma empresa com receita de R$ 10M"}
        ],
        "max_tokens": 200,
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   🤖 Modelo retornado: {result['model']}")
            print(f"   📝 Resposta: {result['choices'][0]['message']['content'][:100]}...")
        else:
            print(f"   ❌ Erro HTTP: {response.status_code}")
            print(f"   📄 Resposta: {response.text}")
    except Exception as e:
        print(f"   ❌ Exceção: {e}")
    
    # Teste 3: Chamada direta com Mistral (controle)
    print("\n3️⃣ TESTE CONTROLE - Mistral direto:")
    payload = {
        "model": "mistral",
        "messages": [
            {"role": "user", "content": "Diga apenas: Teste funcionando!"}
        ],
        "max_tokens": 50,
        "temperature": 0.1
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   🤖 Modelo retornado: {result['model']}")
            print(f"   📝 Resposta: {result['choices'][0]['message']['content']}")
        else:
            print(f"   ❌ Erro HTTP: {response.status_code}")
            print(f"   📄 Resposta: {response.text}")
    except Exception as e:
        print(f"   ❌ Exceção: {e}")
    
    print("\n🏁 Testes concluídos!")

if __name__ == "__main__":
    test_auto_selection()
