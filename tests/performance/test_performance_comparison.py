import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:5000"

def test_single_request(message, request_id):
    """Faz uma única requisição"""
    start_time = time.time()
    
    payload = {
        "model": "auto",
        "messages": [{"role": "user", "content": message}],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(f"{BASE_URL}/v1/chat/completions", json=payload, timeout=120)
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            return {
                "id": request_id,
                "success": True,
                "elapsed": elapsed,
                "response": data['choices'][0]['message']['content'][:50] + "..."
            }
        else:
            return {"id": request_id, "success": False, "error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        return {"id": request_id, "success": False, "error": str(e)}

def test_sequential_vs_concurrent():
    """Compara processamento sequencial vs concorrente"""
    
    messages = [
        "Como vai?",
        "Tudo bem?",
        "Olá!"
    ]
    
    print("🔥 TESTE: SEQUENCIAL vs CONCORRENTE")
    print("=" * 50)
    
    # TESTE SEQUENCIAL
    print("\n1️⃣ PROCESSAMENTO SEQUENCIAL:")
    sequential_start = time.time()
    
    sequential_results = []
    for i, msg in enumerate(messages):
        print(f"   Processando requisição {i+1}...")
        result = test_single_request(msg, i+1)
        sequential_results.append(result)
    
    sequential_time = time.time() - sequential_start
    
    # TESTE CONCORRENTE
    print(f"\n2️⃣ PROCESSAMENTO CONCORRENTE:")
    concurrent_start = time.time()
    
    with ThreadPoolExecutor(max_workers=len(messages)) as executor:
        print(f"   Enviando {len(messages)} requisições simultaneamente...")
        futures = [executor.submit(test_single_request, msg, i+1) for i, msg in enumerate(messages)]
        concurrent_results = [future.result() for future in futures]
    
    concurrent_time = time.time() - concurrent_start
    
    # RESULTADOS
    print(f"\n📊 RESULTADOS:")
    print(f"   ⏱️  Sequencial: {sequential_time:.1f}s")
    print(f"   🚀 Concorrente: {concurrent_time:.1f}s")
    
    if sequential_time > 0:
        speedup = sequential_time / concurrent_time
        print(f"   📈 Speedup: {speedup:.1f}x mais rápido")
        
        time_saved = sequential_time - concurrent_time
        print(f"   ⏰ Tempo economizado: {time_saved:.1f}s")

if __name__ == "__main__":
    test_sequential_vs_concurrent()
