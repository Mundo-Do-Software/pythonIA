import requests
import json
import time

def test_fresh_error():
    """Teste com pergunta nova para verificar validação"""
    
    headers = {
        'X-API-Key': 'dfdjhasdfgldfugydlsuiflhgd',
        'Content-Type': 'application/json'
    }
    
    # Pergunta completamente nova para garantir que não há cache
    unique_question = f"Pergunta única {time.time()}"
    
    payload = {
        "model": "modelo-que-nao-existe:777",  # Modelo que definitivamente não existe
        "messages": [
            {"role": "user", "content": unique_question}
        ],
        "max_tokens": 10
    }
    
    print(f"📤 Pergunta única: {unique_question}")
    print("📤 Modelo inexistente: modelo-que-nao-existe:777")
    
    response = requests.post("http://localhost:5000/v1/chat/completions", 
                           headers=headers, 
                           json=payload, 
                           timeout=15)
    
    if response.status_code == 200:
        data = response.json()
        content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
        print(f"📥 Resposta: {content}")
        
        if "Erro na chamada do Ollama" in content:
            print("⚠️ ERRO DETECTADO - agora vamos ver se a validação funcionou!")
    else:
        print(f"❌ Status: {response.status_code}")

if __name__ == "__main__":
    test_fresh_error()
