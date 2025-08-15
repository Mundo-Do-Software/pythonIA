#!/usr/bin/env python3
"""
Teste simples da API otimizada
"""
import requests
import time
import json

def test_simple():
    url = "http://localhost:5000/v1/chat/completions"
    
    payload = {
        "model": "mistral",
        "messages": [
            {
                "role": "user",
                "content": "Explique o que são fundos imobiliários em poucas palavras"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }
    
    print("🧪 Testando API otimizada...")
    print(f"📤 Enviando: {payload['messages'][0]['content']}")
    
    start_time = time.time()
    
    try:
        response = requests.post(url, json=payload, timeout=120)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            print(f"✅ Sucesso! Tempo: {response_time:.2f}s")
            print(f"📝 Resposta: {content[:200]}...")
            
            if response_time < 30:
                print("🚀 Excelente! < 30s")
            elif response_time < 60:
                print("✅ Bom! < 1 minuto")
            elif response_time < 90:
                print("🔶 OK! < 1.5 minutos") 
            else:
                print("❌ Ainda lento > 1.5 minutos")
                
        else:
            print(f"❌ Erro HTTP {response.status_code}")
            print(f"❌ Resposta: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout após 120s")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_simple()
