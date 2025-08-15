#!/usr/bin/env python3
"""
Testa a API e verifica se o cache está funcionando
"""

import requests
import json
import time
import redis

def test_api_call(content, expected_cache=False):
    """Faz uma chamada à API e verifica o cache"""
    print(f"\n🔄 Testando: {content[:50]}...")
    
    # Fazer chamada à API
    payload = {
        "model": "auto",
        "messages": [{"role": "user", "content": content}]
    }
    
    start_time = time.time()
    
    try:
        response = requests.post(
            "http://localhost:5000/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=60
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Sucesso em {elapsed:.2f}s")
            
            # Verificar se foi cache hit baseado no tempo
            if elapsed < 1.0:
                print(f"⚡ Cache HIT - Muito rápido ({elapsed:.2f}s)")
            else:
                print(f"🔥 Cache MISS - Processamento LLM ({elapsed:.2f}s)")
                
            return True
        else:
            print(f"❌ Erro {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def check_redis_cache():
    """Verifica o estado do cache Redis"""
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        
        # Testar conexão
        r.ping()
        print("✅ Redis conectado")
        
        # Verificar tamanho
        db_size = r.dbsize()
        print(f"📊 Cache entries: {db_size}")
        
        # Listar TODAS as chaves para debug
        all_keys = r.keys("*")
        cache_keys = r.keys("cache:*")
        print(f"🗝️  Total keys: {len(all_keys)}")
        print(f"🗝️  Cache keys encontradas: {len(cache_keys)}")
        
        if all_keys:
            print("🔍 Todas as chaves:")
            for i, key in enumerate(all_keys[:5]):
                print(f"  {i+1}. {key}")
                
        return db_size > 0
        
    except Exception as e:
        print(f"❌ Erro Redis: {e}")
        return False

def main():
    """Teste principal"""
    print("🧪 Teste da API + Cache Redis")
    print("=" * 50)
    
    # 1. Verificar Redis primeiro
    print("\n📊 Verificando estado do Redis...")
    has_cache = check_redis_cache()
    
    # 2. Fazer algumas consultas de teste (menos para evitar timeout)
    test_queries = [
        "Oi",
        "Qual é 2+2?",
        "Oi"  # Repetir para testar cache
    ]
    
    print(f"\n🚀 Executando {len(test_queries)} consultas...")
    
    successful_calls = 0
    for i, query in enumerate(test_queries, 1):
        print(f"\n[{i}/{len(test_queries)}]", end=" ")
        if test_api_call(query):
            successful_calls += 1
        
        # Pausa entre chamadas
        time.sleep(2)
    
    print(f"\n🎯 Resultados:")
    print(f"✅ Sucessos: {successful_calls}/{len(test_queries)}")
    print(f"📊 Taxa de sucesso: {(successful_calls/len(test_queries)*100):.1f}%")
    
    # 3. Verificar cache final
    print(f"\n📊 Estado final do cache:")
    check_redis_cache()

if __name__ == "__main__":
    main()
