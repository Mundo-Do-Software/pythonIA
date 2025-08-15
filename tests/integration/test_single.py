#!/usr/bin/env python3
"""
Teste simples da API com timeout maior
"""

import requests
import json

def test_single_request():
    """Testa uma única requisição"""
    payload = {
        "model": "auto",
        "messages": [
            {
                "role": "user",
                "content": "Olá, como você está?"
            }
        ]
    }
    
    try:
        print("🔄 Fazendo requisição à API...")
        response = requests.post(
            "http://localhost:5000/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=120  # 2 minutos de timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Sucesso!")
            print(f"Resposta: {result['choices'][0]['message']['content']}")
            return True
        else:
            print(f"❌ Erro {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

if __name__ == "__main__":
    test_single_request()
