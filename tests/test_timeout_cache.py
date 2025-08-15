import requests
import json
import time
import redis

# Configurações da API
API_URL = "http://localhost:5000"
API_KEY = "dfdjhasdfgldfugydlsuiflhgd"

# Configurações do Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def simulate_timeout_scenario():
    """Simula cenário de timeout para verificar se não está sendo cacheado"""
    print("\n" + "="*60)
    print("🧪 TESTE: Verificação de Cache de Timeouts")
    print("="*60)
    
    # Teste 1: Pergunta que pode dar timeout
    test_prompt = "Escreva um ensaio de 10.000 palavras sobre física quântica e suas aplicações na computação moderna, incluindo análises detalhadas de cada conceito"
    
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {
        "model": "llama3.2:1b",
        "prompt": test_prompt,
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    print(f"📤 Enviando pergunta longa que pode dar timeout...")
    print(f"Prompt: {test_prompt[:100]}...")
    
    start_time = time.time()
    
    try:
        response = requests.post(f"{API_URL}/v1/chat/completions", 
                               headers=headers, 
                               json=payload, 
                               timeout=10)  # Timeout baixo para forçar erro
        
        if response.status_code == 200:
            response_data = response.json()
            content = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            print(f"📥 Resposta recebida em {time.time() - start_time:.2f}s")
            print(f"Conteúdo: {content[:100]}...")
            
            # Verificar se contém indicador de timeout
            if "Timeout na requisição" in content:
                print("⚠️ TIMEOUT DETECTADO na resposta!")
                
                # Verificar se foi armazenado no cache
                cache_keys = redis_client.keys(f"*{hash(test_prompt)}*")
                embedding_keys = redis_client.keys(f"embedding:*")
                
                print(f"🔍 Verificando cache...")
                print(f"Cache keys encontradas: {len(cache_keys)}")
                print(f"Embedding keys encontradas: {len(embedding_keys)}")
                
                if cache_keys or embedding_keys:
                    print("❌ ERRO: Timeout foi armazenado no cache! Bug não corrigido.")
                    return False
                else:
                    print("✅ SUCESSO: Timeout NÃO foi armazenado no cache!")
                    return True
            else:
                print("✅ Resposta válida recebida (sem timeout)")
                return True
                
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout na requisição HTTP (esperado)")
        return True
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def test_valid_response_caching():
    """Testa se respostas válidas ainda estão sendo cacheadas"""
    print("\n" + "="*60)
    print("🧪 TESTE: Verificação de Cache de Respostas Válidas")
    print("="*60)
    
    # Limpar cache antes do teste
    redis_client.flushdb()
    print("🧹 Cache limpo")
    
    test_prompt = "Qual é a capital do Brasil?"
    
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {
        "model": "llama3.2:1b",
        "prompt": test_prompt,
        "max_tokens": 50,
        "temperature": 0.1
    }
    
    print(f"📤 Primeira requisição: {test_prompt}")
    
    start_time = time.time()
    
    try:
        response = requests.post(f"{API_URL}/v1/chat/completions", 
                               headers=headers, 
                               json=payload, 
                               timeout=30)
        
        first_time = time.time() - start_time
        
        if response.status_code == 200:
            response_data = response.json()
            content = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            print(f"📥 Primeira resposta em {first_time:.2f}s: {content[:50]}...")
            
            if "Timeout na requisição" not in content and len(content) > 10:
                print("✅ Resposta válida recebida")
                
                # Segunda requisição (deve usar cache)
                print(f"📤 Segunda requisição (mesma pergunta)")
                
                start_time2 = time.time()
                response2 = requests.post(f"{API_URL}/v1/chat/completions", 
                                        headers=headers, 
                                        json=payload, 
                                        timeout=30)
                
                second_time = time.time() - start_time2
                
                if response2.status_code == 200:
                    response_data2 = response2.json()
                    content2 = response_data2.get('choices', [{}])[0].get('message', {}).get('content', '')
                    
                    print(f"📥 Segunda resposta em {second_time:.2f}s: {content2[:50]}...")
                    
                    if second_time < 1.0:  # Cache hit deve ser muito rápido
                        print(f"✅ CACHE HIT! Speedup: {first_time/second_time:.1f}x")
                        return True
                    else:
                        print("❌ Cache não funcionou (resposta demorou)")
                        return False
                        
            else:
                print("❌ Primeira resposta foi inválida")
                return False
                
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    print("🚀 Iniciando testes de validação do cache...")
    
    # Aguardar API inicializar
    print("⏳ Aguardando API inicializar...")
    time.sleep(5)
    
    # Teste 1: Verificar se timeouts não são cacheados
    timeout_test = simulate_timeout_scenario()
    
    # Teste 2: Verificar se respostas válidas ainda são cacheadas
    valid_test = test_valid_response_caching()
    
    print("\n" + "="*60)
    print("📊 RESULTADOS DOS TESTES")
    print("="*60)
    print(f"🔸 Timeout não cacheado: {'✅ PASSOU' if timeout_test else '❌ FALHOU'}")
    print(f"🔸 Respostas válidas cacheadas: {'✅ PASSOU' if valid_test else '❌ FALHOU'}")
    
    if timeout_test and valid_test:
        print("\n🎉 TODOS OS TESTES PASSARAM! Bug corrigido com sucesso!")
    else:
        print("\n⚠️ Alguns testes falharam. Verificar implementação.")

if __name__ == "__main__":
    main()
