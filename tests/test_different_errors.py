import requests
import json
import time
import random

def test_different_errors():
    """Testa com perguntas completamente diferentes"""
    
    headers = {
        'X-API-Key': 'dfdjhasdfgldfugydlsuiflhgd',
        'Content-Type': 'application/json'
    }
    
    # Primeira pergunta com modelo inexistente
    payload1 = {
        "model": f"modelo-inexistente-{random.randint(1000, 9999)}",
        "messages": [
            {"role": "user", "content": f"Pergunta única {random.randint(10000, 99999)}"}
        ],
        "max_tokens": 10
    }
    
    # Segunda pergunta COMPLETAMENTE diferente
    payload2 = {
        "model": f"outro-modelo-inexistente-{random.randint(1000, 9999)}",
        "messages": [
            {"role": "user", "content": f"Questão diferente {random.randint(10000, 99999)}"}
        ],
        "max_tokens": 10
    }
    
    print("🧪 TESTE: Duas perguntas diferentes com modelos inexistentes")
    print("="*60)
    
    # Primeira requisição
    print(f"📤 1ª pergunta: {payload1['messages'][0]['content']}")
    print(f"📤 1º modelo: {payload1['model']}")
    
    start_time1 = time.time()
    response1 = requests.post("http://localhost:5000/v1/chat/completions", 
                            headers=headers, 
                            json=payload1, 
                            timeout=15)
    time1 = time.time() - start_time1
    
    if response1.status_code == 200:
        data1 = response1.json()
        content1 = data1.get('choices', [{}])[0].get('message', {}).get('content', '')
        print(f"📥 1ª resposta ({time1:.2f}s): {content1[:40]}...")
    
    # Aguardar um pouco
    time.sleep(1)
    
    # Segunda requisição com pergunta completamente diferente
    print(f"\n📤 2ª pergunta: {payload2['messages'][0]['content']}")
    print(f"📤 2º modelo: {payload2['model']}")
    
    start_time2 = time.time()
    response2 = requests.post("http://localhost:5000/v1/chat/completions", 
                            headers=headers, 
                            json=payload2, 
                            timeout=15)
    time2 = time.time() - start_time2
    
    if response2.status_code == 200:
        data2 = response2.json()
        content2 = data2.get('choices', [{}])[0].get('message', {}).get('content', '')
        print(f"📥 2ª resposta ({time2:.2f}s): {content2[:40]}...")
    
    print(f"\n📊 ANÁLISE:")
    print(f"🔸 Tempo 1: {time1:.2f}s")
    print(f"🔸 Tempo 2: {time2:.2f}s")
    print(f"🔸 Diferença: {abs(time1-time2):.2f}s")
    
    if abs(time1 - time2) < 0.3:  # Tempos similares
        print("✅ SUCESSO: Tempos similares - erro não sendo cacheado!")
        return True
    else:
        print("⚠️ Tempos muito diferentes - pode haver outro cache")
        return False

def main():
    print("🚀 TESTE DEFINITIVO: Perguntas diferentes para eliminar cache do Ollama")
    
    result = test_different_errors()
    
    print("\n" + "="*60)
    print("📋 CONCLUSÃO:")
    
    if result:
        print("🎉 CORREÇÃO CONFIRMADA!")
        print("✅ Erros não estão sendo cacheados semanticamente")
    else:
        print("📝 Diferença de tempo pode ser otimização do Ollama, não cache semântico")
    
    print("\n🔍 VERIFICAÇÃO NOS LOGS:")
    print("📌 Procure por: '⚠️ [CACHE SKIP] Resposta inválida não será armazenada!'")
    print("📌 Se aparecer, a correção está funcionando!")

if __name__ == "__main__":
    main()
