#!/usr/bin/env python3
"""
Teste do Redis Cache integrado
"""
import requests
import time

def test_redis_cache():
    """Testa o cache Redis"""
    url = "http://localhost:5000/v1/chat/completions"
    
    payload = {
        "model": "llama3.2:3b",
        "messages": [
            {
                "role": "user", 
                "content": "O que é um investimento de baixo risco?"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    print("🧪 TESTE DO CACHE REDIS")
    print("=" * 50)
    
    # Primeira requisição (sem cache)
    print("🔄 1ª Requisição (deve ir para Ollama)...")
    start_time = time.time()
    
    try:
        response = requests.post(url, json=payload, timeout=120)
        first_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            print(f"✅ Sucesso! Tempo: {first_time:.2f}s")
            print(f"📝 Resposta: {content[:100]}...")
            
            # Segunda requisição (deve vir do cache Redis)
            print("\n🔄 2ª Requisição (deve vir do Redis)...")
            start_time = time.time()
            
            response2 = requests.post(url, json=payload, timeout=30)
            second_time = time.time() - start_time
            
            if response2.status_code == 200:
                result2 = response2.json()
                
                print(f"✅ Sucesso! Tempo: {second_time:.2f}s")
                
                # Verificar se as respostas são iguais (cache funcionando)
                if result['choices'][0]['message']['content'] == result2['choices'][0]['message']['content']:
                    print(f"🎯 Cache funcionando! Respostas idênticas")
                else:
                    print(f"⚠️ Respostas diferentes - pode não estar usando cache")
                
                # Calcular melhoria de performance
                if second_time < first_time * 0.1:  # Cache deve ser 10x mais rápido
                    speedup = first_time / second_time
                    print(f"🚀 REDIS CACHE ATIVO! Melhoria de {speedup:.1f}x")
                    print(f"💾 {first_time:.2f}s → {second_time:.2f}s")
                else:
                    print(f"⚠️ Cache pode não estar ativo (esperado <{first_time*0.1:.2f}s)")
                
                return first_time, second_time
            else:
                print(f"❌ Erro na 2ª requisição: {response2.status_code}")
                
        else:
            print(f"❌ Erro na 1ª requisição: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None, None

if __name__ == "__main__":
    test_redis_cache()
