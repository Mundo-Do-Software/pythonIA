#!/usr/bin/env python3

import requests
import json

def test_ollama_models():
    base_url = "http://localhost:11434"
    
    # Testar disponibilidade
    try:
        tags_response = requests.get(f"{base_url}/api/tags")
        print(f"📋 Modelos disponíveis:")
        for model in tags_response.json()["models"]:
            print(f"   ✅ {model['name']}")
    except Exception as e:
        print(f"❌ Erro ao listar modelos: {e}")
        return
    
    # Testar Llama 3.2
    print(f"\n🔸 Testando Llama 3.2:")
    try:
        response = requests.post(f"{base_url}/api/generate", 
            json={
                "model": "llama3.2:3b",
                "prompt": "Diga apenas: Hello World!",
                "stream": False
            },
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Resposta: {result.get('response', 'N/A')}")
        else:
            print(f"   ❌ Erro {response.status_code}: {response.text}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Testar Mistral
    print(f"\n🔸 Testando Mistral:")
    try:
        response = requests.post(f"{base_url}/api/generate", 
            json={
                "model": "mistral:latest",
                "prompt": "Diga apenas: Hello World!",
                "stream": False
            },
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Resposta: {result.get('response', 'N/A')}")
        else:
            print(f"   ❌ Erro {response.status_code}: {response.text}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")

if __name__ == "__main__":
    test_ollama_models()
