#!/usr/bin/env python3
"""
Teste com modelo menor para comparar performance
"""
import requests
import time

def test_with_smaller_model():
    url = "http://localhost:5000/v1/chat/completions"
    
    payload = {
        "model": "llama3.2:3b",  # Modelo menor
        "messages": [
            {
                "role": "user", 
                "content": "O que é diversificação de investimentos? Resposta breve."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    print("🧪 Testando com modelo menor (llama3.2:3b)...")
    
    start_time = time.time()
    
    try:
        response = requests.post(url, json=payload, timeout=120)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            print(f"✅ Sucesso! Tempo: {response_time:.2f}s")
            print(f"📝 Resposta: {content}")
            
            if response_time < 20:
                print("🚀 Muito rápido! < 20s")
            elif response_time < 40:
                print("✅ Rápido! < 40s")
            elif response_time < 60:
                print("🔶 OK! < 1 minuto")
            else:
                print("❌ Ainda lento > 1 minuto")
                
        else:
            print(f"❌ Erro HTTP {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_with_smaller_model()
