#!/usr/bin/env python3
"""
Teste completo da API com modelo Gemma2
"""

import requests
import json
import time
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

API_BASE_URL = "http://localhost:5000"
TIMEOUT = 60  # Timeout generoso para o Gemma2

def test_api_health():
    """Verifica se a API está funcionando"""
    print("🏥 Testando saúde da API...")
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=10)
        print(f"✅ API responde: {response.status_code}")
        if response.status_code == 200:
            print(f"📋 Resposta: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ API não está respondendo: {e}")
        return False

def test_models_endpoint():
    """Verifica os modelos disponíveis"""
    print("\n🤖 Testando endpoint de modelos...")
    try:
        response = requests.get(f"{API_BASE_URL}/v1/models", timeout=10)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Modelos disponíveis:")
            for model in models.get('data', []):
                print(f"   - {model.get('id', 'N/A')}")
            
            # Verificar se Gemma2 está disponível
            model_ids = [m.get('id', '') for m in models.get('data', [])]
            gemma_models = [m for m in model_ids if 'gemma' in m.lower()]
            if gemma_models:
                print(f"🎯 Modelos Gemma encontrados: {gemma_models}")
                return gemma_models[0]  # Retorna o primeiro modelo Gemma encontrado
            else:
                print("⚠️  Nenhum modelo Gemma encontrado, usando gemma2:2b")
                return "gemma2:2b"
        else:
            print(f"❌ Erro ao listar modelos: {response.status_code}")
            return "gemma2:2b"
    except Exception as e:
        print(f"❌ Erro ao verificar modelos: {e}")
        return "gemma2:2b"

def test_simple_request(model="gemma2:2b"):
    """Teste uma requisição simples com Gemma2"""
    print(f"\n🧪 Teste Simples - Modelo: {model}")
    print("=" * 50)
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Olá! Você pode me dizer qual é a capital do Brasil?"}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    print(f"📤 Enviando requisição...")
    print(f"🗯️  Pergunta: {payload['messages'][0]['content']}")
    
    try:
        start_time = time.time()
        
        response = requests.post(
            f"{API_BASE_URL}/v1/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"⏱️  Tempo: {response_time:.2f}s")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Extrair resposta
            if data.get('choices') and len(data['choices']) > 0:
                message_content = data['choices'][0].get('message', {}).get('content', '')
                print(f"🤖 Resposta do Gemma2: {message_content}")
                
                # Mostrar estatísticas de uso
                usage = data.get('usage', {})
                if usage:
                    print(f"📊 Tokens usados: {usage}")
                
                return True
            else:
                print("❌ Resposta sem conteúdo")
                print(f"📋 JSON completo: {json.dumps(data, indent=2, ensure_ascii=False)}")
                return False
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            try:
                error_data = response.json()
                print(f"📋 Erro: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"📋 Resposta raw: {response.text}")
            return False
            
    except requests.Timeout:
        print(f"⏰ Timeout após {TIMEOUT}s")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_conversation(model="gemma2:2b"):
    """Teste uma conversa com múltiplas mensagens"""
    print(f"\n💬 Teste de Conversa - Modelo: {model}")
    print("=" * 50)
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Você é um assistente útil e responde em português brasileiro."},
            {"role": "user", "content": "Qual é a capital do Brasil?"},
            {"role": "assistant", "content": "A capital do Brasil é Brasília."},
            {"role": "user", "content": "E qual é a população de Brasília?"}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    print("📤 Testando conversa com contexto...")
    
    try:
        start_time = time.time()
        
        response = requests.post(
            f"{API_BASE_URL}/v1/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"⏱️  Tempo: {response_time:.2f}s")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('choices') and len(data['choices']) > 0:
                message_content = data['choices'][0].get('message', {}).get('content', '')
                print(f"🤖 Resposta do Gemma2: {message_content}")
                return True
            else:
                print("❌ Resposta sem conteúdo")
                return False
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_technical_question(model="gemma2:2b"):
    """Teste uma pergunta técnica"""
    print(f"\n🔧 Teste Técnico - Modelo: {model}")
    print("=" * 50)
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Explique o que é uma API REST em termos simples."}
        ],
        "temperature": 0.5,  # Menor temperatura para resposta mais focada
        "max_tokens": 200
    }
    
    print("📤 Testando pergunta técnica...")
    
    try:
        start_time = time.time()
        
        response = requests.post(
            f"{API_BASE_URL}/v1/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"⏱️  Tempo: {response_time:.2f}s")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('choices') and len(data['choices']) > 0:
                message_content = data['choices'][0].get('message', {}).get('content', '')
                print(f"🤖 Resposta do Gemma2: {message_content}")
                return True
            else:
                print("❌ Resposta sem conteúdo")
                return False
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_performance(model="gemma2:2b", num_requests=3):
    """Teste de performance com múltiplas requisições"""
    print(f"\n⚡ Teste de Performance - {num_requests} requisições")
    print("=" * 50)
    
    def single_request(i):
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": f"Esta é a pergunta número {i+1}. Responda brevemente."}
            ],
            "temperature": 0.7,
            "max_tokens": 50
        }
        
        start_time = time.time()
        try:
            response = requests.post(
                f"{API_BASE_URL}/v1/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=TIMEOUT
            )
            end_time = time.time()
            return {
                "request": i+1,
                "status": response.status_code,
                "time": end_time - start_time,
                "success": response.status_code == 200
            }
        except Exception as e:
            end_time = time.time()
            return {
                "request": i+1,
                "status": "error",
                "time": end_time - start_time,
                "success": False,
                "error": str(e)
            }
    
    print("📤 Enviando requisições sequenciais...")
    results = []
    
    for i in range(num_requests):
        print(f"📨 Requisição {i+1}/{num_requests}...")
        result = single_request(i)
        results.append(result)
        print(f"   ⏱️  {result['time']:.2f}s - Status: {result['status']}")
    
    # Estatísticas
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"\n📊 Resultados do Teste de Performance:")
    print(f"   ✅ Sucessos: {len(successful)}/{num_requests}")
    print(f"   ❌ Falhas: {len(failed)}/{num_requests}")
    
    if successful:
        times = [r['time'] for r in successful]
        print(f"   ⏱️  Tempo médio: {sum(times)/len(times):.2f}s")
        print(f"   ⏱️  Tempo mínimo: {min(times):.2f}s")
        print(f"   ⏱️  Tempo máximo: {max(times):.2f}s")
    
    return len(successful) == num_requests

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando Testes do Gemma2")
    print("=" * 60)
    
    # 1. Verificar se a API está funcionando
    if not test_api_health():
        print("❌ API não está disponível. Verifique se o servidor está rodando.")
        return
    
    # 2. Verificar modelos disponíveis
    model = test_models_endpoint()
    
    # 3. Executar testes
    tests = [
        ("Teste Simples", lambda: test_simple_request(model)),
        ("Teste de Conversa", lambda: test_conversation(model)),
        ("Teste Técnico", lambda: test_technical_question(model)),
        ("Teste de Performance", lambda: test_performance(model, 3))
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro no {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📋 RESUMO DOS TESTES")
    print("=" * 60)
    
    successful = 0
    for test_name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{status} - {test_name}")
        if success:
            successful += 1
    
    print(f"\n🎯 Resultado Final: {successful}/{len(results)} testes passaram")
    
    if successful == len(results):
        print("🎉 Todos os testes passaram! O Gemma2 está funcionando perfeitamente.")
    else:
        print("⚠️  Alguns testes falharam. Verifique os logs acima.")

if __name__ == "__main__":
    main()
