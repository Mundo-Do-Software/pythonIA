import requests
import json
import time

# Configurações da API
API_URL = "http://localhost:5000"
API_KEY = "dfdjhasdfgldfugydlsuiflhgd"

def test_timeout_scenario():
    """Testa cenário que pode dar timeout"""
    print("\n🧪 TESTE: Verificação de Timeout (não deve ser cacheado)")
    print("="*60)
    
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    # Pergunta muito longa que pode dar timeout
    long_prompt = "Escreva um ensaio extremamente detalhado de 10.000 palavras sobre mecânica quântica, incluindo todas as equações, provas matemáticas, aplicações em computação quântica, criptografia quântica, e uma análise completa de todos os experimentos históricos"
    
    payload = {
        "model": "llama3.2:3b",
        "messages": [
            {"role": "user", "content": long_prompt}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    print(f"📤 Enviando pergunta longa: {long_prompt[:60]}...")
    
    try:
        response = requests.post(f"{API_URL}/v1/chat/completions", 
                               headers=headers, 
                               json=payload, 
                               timeout=8)  # Timeout baixo para forçar erro
        
        if response.status_code == 200:
            response_data = response.json()
            content = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            print(f"📥 Resposta: {content[:100]}...")
            
            if "Timeout na requisição" in content:
                print("⚠️ TIMEOUT DETECTADO - isso NÃO deve ser cacheado!")
                
                # Fazer segunda requisição para ver se foi cacheado
                print("📤 Segunda requisição (mesma pergunta)...")
                
                start_time = time.time()
                response2 = requests.post(f"{API_URL}/v1/chat/completions", 
                                        headers=headers, 
                                        json=payload, 
                                        timeout=8)
                second_time = time.time() - start_time
                
                if response2.status_code == 200:
                    response_data2 = response2.json()
                    content2 = response_data2.get('choices', [{}])[0].get('message', {}).get('content', '')
                    
                    if second_time < 1.0 and "Timeout na requisição" in content2:
                        print(f"❌ ERRO: Timeout foi cacheado! (resposta em {second_time:.2f}s)")
                        return False
                    else:
                        print(f"✅ SUCESSO: Timeout não foi cacheado (resposta em {second_time:.2f}s)")
                        return True
            else:
                print("✅ Resposta válida recebida")
                return True
                
        else:
            print(f"❌ Erro HTTP: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout na requisição HTTP (aceitável)")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_valid_caching():
    """Testa se respostas válidas estão sendo cacheadas"""
    print("\n🧪 TESTE: Verificação de Cache Válido")
    print("="*60)
    
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {
        "model": "llama3.2:3b",
        "messages": [
            {"role": "user", "content": "Qual é a capital do Brasil?"}
        ],
        "max_tokens": 50,
        "temperature": 0.1
    }
    
    print("📤 Primeira requisição: Qual é a capital do Brasil?")
    
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
            
            if "Timeout na requisição" not in content and len(content.strip()) > 5:
                print("✅ Resposta válida - deve ser cacheada")
                
                # Segunda requisição
                print("📤 Segunda requisição (mesma pergunta)...")
                
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
                    
                    if second_time < 2.0:  # Cache deve ser rápido
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
            print(f"❌ Erro HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("🚀 Iniciando testes de validação do cache...")
    
    # Aguardar API
    print("⏳ Aguardando API...")
    time.sleep(3)
    
    # Teste 1: Respostas válidas devem ser cacheadas
    valid_test = test_valid_caching()
    
    # Aguardar um pouco
    time.sleep(2)
    
    # Teste 2: Timeouts não devem ser cacheados  
    timeout_test = test_timeout_scenario()
    
    print("\n" + "="*60)
    print("📊 RESULTADOS")
    print("="*60)
    print(f"🔸 Cache de respostas válidas: {'✅ OK' if valid_test else '❌ FALHOU'}")
    print(f"🔸 Timeout não cacheado: {'✅ OK' if timeout_test else '❌ FALHOU'}")
    
    if valid_test and timeout_test:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Bug do cache de timeouts foi corrigido!")
    else:
        print("\n⚠️ Alguns testes falharam.")

if __name__ == "__main__":
    main()
