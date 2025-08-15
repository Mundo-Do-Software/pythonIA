import asyncio
import aiohttp
import time
import json

BASE_URL = "http://localhost:5000"

async def test_concurrent_request(session, request_id, message):
    """Faz uma requisição individual"""
    start_time = time.time()
    
    payload = {
        "model": "auto",
        "messages": [{"role": "user", "content": message}],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        async with session.post(
            f"{BASE_URL}/v1/chat/completions", 
            json=payload,
            timeout=aiohttp.ClientTimeout(total=120)
        ) as response:
            
            if response.status == 200:
                data = await response.json()
                elapsed = time.time() - start_time
                
                return {
                    "id": request_id,
                    "success": True,
                    "elapsed": elapsed,
                    "model": data.get('model', 'N/A'),
                    "response": data['choices'][0]['message']['content'][:100] + "...",
                    "message": message
                }
            else:
                error = await response.text()
                return {
                    "id": request_id,
                    "success": False,
                    "error": f"HTTP {response.status}: {error}",
                    "message": message
                }
                
    except Exception as e:
        return {
            "id": request_id,
            "success": False,
            "error": str(e),
            "message": message
        }

async def test_concurrency():
    """Testa múltiplas requisições simultâneas"""
    
    print("🚀 TESTE DE CONCORRÊNCIA")
    print("=" * 50)
    
    # Diferentes tipos de mensagens para testar seleção de modelos
    test_messages = [
        "Oi, tudo bem?",  # Simples -> Llama 3.2
        "Analisar KPIs: Receita R$ 1M, Margem 30%",  # Complexo -> Mistral
        "Como vai você?",  # Simples -> Llama 3.2
        "Diagnóstico financeiro da empresa",  # Complexo -> Mistral
        "Obrigado pela ajuda!",  # Simples -> Llama 3.2
        "Estratégia de marketing digital avançada"  # Complexo -> Mistral
    ]
    
    print(f"📋 Enviando {len(test_messages)} requisições simultâneas...")
    
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        # Criar todas as tarefas
        tasks = [
            test_concurrent_request(session, i+1, msg)
            for i, msg in enumerate(test_messages)
        ]
        
        # Executar todas simultaneamente
        results = await asyncio.gather(*tasks, return_exceptions=True)
    
    total_time = time.time() - start_time
    
    print(f"\n⏱️  RESULTADOS APÓS {total_time:.2f}s")
    print("=" * 50)
    
    successful = 0
    failed = 0
    
    for result in results:
        if isinstance(result, Exception):
            print(f"❌ Exceção: {result}")
            failed += 1
        elif result['success']:
            print(f"✅ Req {result['id']:2d}: {result['elapsed']:5.1f}s | {result['model']:8s} | \"{result['message'][:30]}...\"")
            successful += 1
        else:
            print(f"❌ Req {result['id']:2d}: FALHOU | {result['error']}")
            failed += 1
    
    print(f"\n📊 RESUMO:")
    print(f"   ✅ Sucessos: {successful}")
    print(f"   ❌ Falhas: {failed}")
    print(f"   ⏱️  Tempo total: {total_time:.2f}s")
    print(f"   🚀 Requisições por segundo: {len(test_messages)/total_time:.2f}")
    
    if successful > 0:
        avg_time = sum(r['elapsed'] for r in results if isinstance(r, dict) and r['success']) / successful
        print(f"   ⏱️  Tempo médio por requisição: {avg_time:.2f}s")

if __name__ == "__main__":
    asyncio.run(test_concurrency())
