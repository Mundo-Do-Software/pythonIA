#!/usr/bin/env python3

import requests
import json

def test_system():
    print("🧪 TESTE COMPLETO DO SISTEMA")
    print("=" * 50)
    
    try:
        # 1. Health Check
        print("\n1️⃣ HEALTH CHECK:")
        health = requests.get("http://localhost:5000/").json()
        print(f"   Status: {health}")
        
        # 2. Lista de modelos
        print("\n2️⃣ LISTA DE MODELOS:")
        models = requests.get("http://localhost:5000/v1/models").json()
        print(f"   Modelos: {json.dumps(models, indent=2)}")
        
        # 3. Teste com Mistral direto
        print("\n3️⃣ TESTE MISTRAL:")
        payload = {
            "model": "mistral",
            "messages": [{"role": "user", "content": "Responda apenas: OK"}],
            "max_tokens": 10
        }
        
        response = requests.post("http://localhost:5000/v1/chat/completions", json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Resposta: {result['choices'][0]['message']['content']}")
        else:
            print(f"   ❌ Erro: {response.status_code}")
        
        # 4. Teste com modelo AUTO
        print("\n4️⃣ TESTE AUTO:")
        payload = {
            "model": "auto",
            "messages": [{"role": "user", "content": "Olá, como vai?"}],
            "max_tokens": 20
        }
        
        response = requests.post("http://localhost:5000/v1/chat/completions", json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Resposta: {result['choices'][0]['message']['content']}")
        else:
            print(f"   ❌ Erro: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")

if __name__ == "__main__":
    test_system()
