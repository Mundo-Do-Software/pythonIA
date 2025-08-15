import requests
import json
import time

def test_basic_api():
    """Teste básico da API"""
    print("🧪 Teste básico da API...")
    
    headers = {
        'X-API-Key': 'dfdjhasdfgldfugydlsuiflhgd',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "model": "mistral:latest",
        "messages": [
            {"role": "user", "content": "Diga apenas: Brasil"}
        ],
        "max_tokens": 10,
        "temperature": 0.1
    }
    
    try:
        print("📤 Enviando pergunta simples...")
        response = requests.post("http://localhost:5000/v1/chat/completions", 
                               headers=headers, 
                               json=payload, 
                               timeout=60)
        
        print(f"📥 Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(f"📝 Resposta: {content}")
            
            if "Timeout na requisição" in content or "Erro na chamada" in content:
                print("⚠️ Resposta contém erro - NÃO deve ser cacheada")
            else:
                print("✅ Resposta válida - deve ser cacheada")
        else:
            print(f"❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_basic_api()
