import requests
import json
import time

def test_error_caching():
    """Testa se erros são cacheados (não devem ser)"""
    print("🧪 Teste de cache de erros...")
    
    headers = {
        'X-API-Key': 'dfdjhasdfgldfugydlsuiflhgd',
        'Content-Type': 'application/json'
    }
    
    # Usar um modelo que não existe para forçar erro
    payload = {
        "model": "modelo-inexistente:1b",
        "messages": [
            {"role": "user", "content": "Teste"}
        ],
        "max_tokens": 10,
        "temperature": 0.1
    }
    
    print("📤 Primeira requisição (modelo inexistente)...")
    
    # Primeira requisição - deve retornar erro
    start_time = time.time()
    response1 = requests.post("http://localhost:5000/v1/chat/completions", 
                            headers=headers, 
                            json=payload, 
                            timeout=30)
    
    first_time = time.time() - start_time
    
    if response1.status_code == 200:
        data1 = response1.json()
        content1 = data1.get('choices', [{}])[0].get('message', {}).get('content', '')
        print(f"📝 Primeira resposta ({first_time:.2f}s): {content1[:50]}...")
        
        if "Erro na chamada do Ollama" in content1 or "404" in content1:
            print("⚠️ ERRO DETECTADO - testando se foi cacheado...")
            
            # Segunda requisição - se for cacheada será muito rápida
            print("📤 Segunda requisição (mesma pergunta)...")
            
            start_time2 = time.time()
            response2 = requests.post("http://localhost:5000/v1/chat/completions", 
                                    headers=headers, 
                                    json=payload, 
                                    timeout=30)
            
            second_time = time.time() - start_time2
            
            if response2.status_code == 200:
                data2 = response2.json()
                content2 = data2.get('choices', [{}])[0].get('message', {}).get('content', '')
                print(f"📝 Segunda resposta ({second_time:.2f}s): {content2[:50]}...")
                
                # Se a segunda requisição for muito rápida, foi cacheada
                if second_time < 0.5:
                    print(f"❌ ERRO CACHEADO! Speedup: {first_time/second_time:.1f}x")
                    print("🚨 BUG: Erro está sendo armazenado no cache!")
                    return False
                else:
                    print(f"✅ ERRO NÃO CACHEADO! Tempo similar: {second_time:.2f}s")
                    print("🎉 Cache funcionando corretamente!")
                    return True
        else:
            print("✅ Resposta válida (modelo foi encontrado)")
            return True
    else:
        print(f"❌ Erro HTTP: {response1.status_code}")
        return False

def test_valid_caching():
    """Testa se respostas válidas são cacheadas"""
    print("\n🧪 Teste de cache de respostas válidas...")
    
    headers = {
        'X-API-Key': 'dfdjhasdfgldfugydlsuiflhgd',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "model": "mistral:latest",
        "messages": [
            {"role": "user", "content": "Diga apenas: OK"}
        ],
        "max_tokens": 5,
        "temperature": 0.1
    }
    
    print("📤 Primeira requisição válida...")
    
    start_time = time.time()
    response1 = requests.post("http://localhost:5000/v1/chat/completions", 
                            headers=headers, 
                            json=payload, 
                            timeout=30)
    
    first_time = time.time() - start_time
    
    if response1.status_code == 200:
        data1 = response1.json()
        content1 = data1.get('choices', [{}])[0].get('message', {}).get('content', '')
        print(f"📝 Primeira resposta ({first_time:.2f}s): {content1[:30]}...")
        
        if "Erro" not in content1 and len(content1.strip()) > 0:
            print("✅ Resposta válida - deve ser cacheada")
            
            # Segunda requisição
            print("📤 Segunda requisição (mesma pergunta)...")
            
            start_time2 = time.time()
            response2 = requests.post("http://localhost:5000/v1/chat/completions", 
                                    headers=headers, 
                                    json=payload, 
                                    timeout=30)
            
            second_time = time.time() - start_time2
            
            if response2.status_code == 200:
                data2 = response2.json()
                content2 = data2.get('choices', [{}])[0].get('message', {}).get('content', '')
                print(f"📝 Segunda resposta ({second_time:.2f}s): {content2[:30]}...")
                
                if second_time < 1.0:
                    speedup = first_time / second_time if second_time > 0 else 0
                    print(f"✅ CACHE HIT! Speedup: {speedup:.1f}x")
                    return True
                else:
                    print("❌ Cache não funcionou")
                    return False
        else:
            print("❌ Resposta inválida")
            return False
    else:
        print(f"❌ Erro HTTP: {response1.status_code}")
        return False

def main():
    print("🚀 Testando correção do cache de erros...")
    
    # Teste 1: Respostas válidas devem ser cacheadas
    valid_cache = test_valid_caching()
    
    time.sleep(2)
    
    # Teste 2: Erros não devem ser cacheados
    error_cache = test_error_caching()
    
    print("\n" + "="*60)
    print("📊 RESULTADOS FINAIS")
    print("="*60)
    print(f"🔸 Cache de respostas válidas: {'✅ OK' if valid_cache else '❌ FALHOU'}")
    print(f"🔸 Erro não cacheado: {'✅ OK' if error_cache else '❌ FALHOU'}")
    
    if valid_cache and error_cache:
        print("\n🎉 SUCESSO TOTAL!")
        print("✅ Bug do cache de erros foi corrigido!")
        print("✅ Cache semântico funciona apenas para respostas válidas!")
    else:
        print("\n⚠️ Verificar implementação.")

if __name__ == "__main__":
    main()
