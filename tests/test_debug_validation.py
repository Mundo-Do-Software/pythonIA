import requests
import json

def test_error_validation():
    """Teste rápido para verificar se erro é validado"""
    
    headers = {
        'X-API-Key': 'dfdjhasdfgldfugydlsuiflhgd',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "model": "modelo-inexistente:1b",
        "messages": [
            {"role": "user", "content": "Teste erro"}
        ],
        "max_tokens": 10
    }
    
    print("📤 Testando modelo inexistente para verificar validação...")
    
    response = requests.post("http://localhost:5000/v1/chat/completions", 
                           headers=headers, 
                           json=payload, 
                           timeout=15)
    
    if response.status_code == 200:
        data = response.json()
        content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
        print(f"📥 Resposta: {content}")
    else:
        print(f"❌ Status: {response.status_code}")

if __name__ == "__main__":
    test_error_validation()
