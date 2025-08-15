#!/usr/bin/env python3
"""
Teste simples do modelo fine-tuned
"""

import requests
import json
import time

def test_single_request():
    """Teste uma requisição simples"""
    print("🧪 Teste Simples do Modelo Fine-Tuned")
    print("=" * 50)
    
    # Teste básico
    payload = {
        "model": "mistral",
        "messages": [
            {"role": "user", "content": "Como faço para cancelar meu pedido?"}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    print("📤 Enviando requisição...")
    print(f"🗯️  Pergunta: {payload['messages'][0]['content']}")
    
    try:
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:5000/v1/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30  # Timeout menor para teste
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"⏱️  Tempo: {response_time:.2f}s")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Mostrar dados brutos para debug
            print(f"\n📋 Resposta JSON:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Extrair conteúdo
            choices = data.get('choices', [])
            if choices:
                message_content = choices[0].get('message', {}).get('content', 'N/A')
                print(f"\n🤖 Resposta: {message_content}")
            
            # Verificar se foi usado fine-tuning
            if data.get('fine_tuned'):
                print(f"🧠 Fine-tuned: ✅ ({data.get('domain', 'unknown')})")
                print(f"🎯 Confiança: {data.get('confidence', 0):.1%}")
            else:
                print(f"🧠 Fine-tuned: ❌ (Ollama usado)")
                
            print(f"⚙️  Backend: {data.get('backend', 'unknown')}")
            
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"📄 Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    test_single_request()
