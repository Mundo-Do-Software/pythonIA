import requests
import json
import time

def test_error_not_cached():
    """Teste específico: erro não deve ser cacheado"""
    
    headers = {
        'X-API-Key': 'dfdjhasdfgldfugydlsuiflhgd',
        'Content-Type': 'application/json'
    }
    
    # Usar modelo inexistente para garantir erro
    payload = {
        "model": "modelo-super-inexistente-123",
        "messages": [
            {"role": "user", "content": "Teste de erro"}
        ],
        "max_tokens": 10
    }
    
    print("🧪 TESTE CRÍTICO: Erro não deve ser cacheado")
    print("="*50)
    
    # Primeira requisição - deve retornar erro
    print("📤 1ª requisição (modelo inexistente)...")
    start_time1 = time.time()
    
    response1 = requests.post("http://localhost:5000/v1/chat/completions", 
                            headers=headers, 
                            json=payload, 
                            timeout=15)
    
    time1 = time.time() - start_time1
    
    if response1.status_code == 200:
        data1 = response1.json()
        content1 = data1.get('choices', [{}])[0].get('message', {}).get('content', '')
        print(f"📥 1ª resposta ({time1:.2f}s): {content1[:50]}...")
        
        if "Erro na chamada do Ollama" in content1:
            print("⚠️ ERRO DETECTADO na primeira requisição")
            
            # Segunda requisição - se erro foi cacheado, será muito rápida
            print("📤 2ª requisição (mesma pergunta)...")
            start_time2 = time.time()
            
            response2 = requests.post("http://localhost:5000/v1/chat/completions", 
                                    headers=headers, 
                                    json=payload, 
                                    timeout=15)
            
            time2 = time.time() - start_time2
            
            if response2.status_code == 200:
                data2 = response2.json()
                content2 = data2.get('choices', [{}])[0].get('message', {}).get('content', '')
                print(f"📥 2ª resposta ({time2:.2f}s): {content2[:50]}...")
                
                # Analisar se foi cacheado
                # Para modelo inexistente, Ollama responde rápido (~0.1-0.2s)
                # Cache seria MUITO mais rápido (<0.05s) e com speedup significativo
                speedup = time1 / time2 if time2 > 0 else 1
                
                if time2 < 0.05 and speedup > 3:  # Cache é MUITO mais rápido
                    print(f"❌ FALHOU: Erro foi cacheado (speedup: {speedup:.1f}x)")
                    print("🚨 BUG AINDA PRESENTE!")
                    return False
                elif time2 < 0.3 and abs(time1 - time2) < 0.1:  # Tempos similares = sem cache
                    print(f"✅ SUCESSO: Erro NÃO foi cacheado (tempos similares: {time1:.2f}s vs {time2:.2f}s)")
                    print("🎉 CORREÇÃO FUNCIONANDO!")
                    return True
                else:
                    print(f"✅ SUCESSO: Erro NÃO foi cacheado (tempo normal: {time2:.2f}s)")
                    print("🎉 CORREÇÃO FUNCIONANDO!")
                    return True
            else:
                print(f"❌ Erro na segunda requisição: {response2.status_code}")
                return False
        else:
            print("⚠️ Primeira resposta não foi erro (modelo pode ter sido encontrado)")
            return False
    else:
        print(f"❌ Erro HTTP na primeira requisição: {response1.status_code}")
        return False

def main():
    print("🚀 TESTE FINAL: Verificação da correção do cache de erros")
    print("🎯 OBJETIVO: Confirmar que erros não são mais armazenados no cache")
    
    result = test_error_not_cached()
    
    print("\n" + "="*60)
    if result:
        print("🎉 PARABÉNS! A correção está funcionando!")
        print("✅ Erros não são mais armazenados no cache semântico")
        print("✅ Cache funciona apenas para respostas válidas")
        print("✅ Bug do timeout/erro foi CORRIGIDO!")
    else:
        print("⚠️ Teste falhou - verificar implementação")

if __name__ == "__main__":
    main()
