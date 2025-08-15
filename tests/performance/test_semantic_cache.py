#!/usr/bin/env python3
"""
Teste do Cache Semântico - perguntas similares mas escritas diferente
"""
import requests
import time

def test_semantic_cache():
    """Testa o cache semântico com perguntas similares"""
    url = "http://localhost:5000/v1/chat/completions"
    
    # Perguntas sobre o mesmo tópico, mas escritas diferente
    questions = [
        "O que são fundos imobiliários?",
        "Me explique sobre fundos imobiliários",
        "Como funcionam os fundos imobiliários?",
        "Explique fundos de investimento imobiliário",
        "O que você sabe sobre FIIs?"
    ]
    
    print("🧠 TESTE DO CACHE SEMÂNTICO")
    print("=" * 60)
    print("🎯 Objetivo: Testar se perguntas similares retornam do cache")
    print()
    
    results = []
    
    for i, question in enumerate(questions, 1):
        payload = {
            "model": "llama3.2:3b",
            "messages": [
                {
                    "role": "user", 
                    "content": question
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }
        
        print(f"🔄 Pergunta {i}: '{question}'")
        start_time = time.time()
        
        try:
            response = requests.post(url, json=payload, timeout=120)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                print(f"✅ Resposta: {response_time:.2f}s")
                print(f"📝 {content[:80]}...")
                
                # Classificar tipo de resposta baseado no tempo
                if response_time < 1:
                    cache_type = "🚀 CACHE SEMÂNTICO"
                elif response_time < 30:
                    cache_type = "⚡ RESPOSTA RÁPIDA"
                else:
                    cache_type = "🔥 PROCESSAMENTO NOVO"
                
                print(f"🏷️  {cache_type}")
                
                results.append({
                    "question": question,
                    "time": response_time,
                    "cache_type": cache_type,
                    "response": content
                })
                
            else:
                print(f"❌ Erro: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            
        print("-" * 60)
        time.sleep(2)  # Pausa entre requisições
    
    # Análise dos resultados
    print("\n📊 ANÁLISE DOS RESULTADOS:")
    print("=" * 60)
    
    cache_hits = [r for r in results if r["time"] < 1]
    fast_responses = [r for r in results if 1 <= r["time"] < 30]
    new_processing = [r for r in results if r["time"] >= 30]
    
    print(f"🎯 Cache semântico hits: {len(cache_hits)}")
    print(f"⚡ Respostas rápidas: {len(fast_responses)}")
    print(f"🔥 Processamento novo: {len(new_processing)}")
    
    if len(cache_hits) > 1:
        print(f"\n🚀 CACHE SEMÂNTICO FUNCIONANDO!")
        print(f"   Perguntas similares foram detectadas e respondidas instantaneamente!")
        
        # Mostrar quais foram do cache
        print(f"\n📝 Perguntas que retornaram do cache:")
        for hit in cache_hits:
            print(f"   • '{hit['question']}' - {hit['time']:.3f}s")
    
    elif len(results) > 0:
        avg_time = sum(r["time"] for r in results) / len(results)
        print(f"\n📊 Tempo médio de resposta: {avg_time:.2f}s")
        
        if avg_time < 5:
            print("✅ Sistema funcionando muito bem!")
        elif avg_time < 60:
            print("🔶 Sistema funcionando adequadamente")
        else:
            print("⚠️ Sistema pode precisar de otimização")

if __name__ == "__main__":
    test_semantic_cache()
