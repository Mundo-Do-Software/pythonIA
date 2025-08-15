#!/usr/bin/env python3
"""
Teste simples da API de chat
"""
import requests
import json

# Configurações
API_URL = "http://localhost:5000"

def test_health():
    """Testa o health check"""
    try:
        response = requests.get(f"{API_URL}/")
        print(f"🏥 Health Check: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro no health check: {e}")
        return False

def test_models():
    """Lista modelos disponíveis"""
    try:
        response = requests.get(f"{API_URL}/v1/models")
        print(f"📋 Modelos: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro ao listar modelos: {e}")
        return False

def test_chat(message="Olá! Como você está?"):
    """Testa uma conversa"""
    try:
        payload = {
            "model": "mistral",
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "temperature": 0.7,
            "max_tokens": 150
        }
        
        print(f"💬 Enviando: {message}")
        response = requests.post(
            f"{API_URL}/v1/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
            print(f"🤖 Resposta: {reply}")
            return True
        else:
            print(f"❌ Erro HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na conversa: {e}")
        return False

def main():
    print("🧪 Testando API de Chat...")
    print("=" * 50)
    
    # Teste 1: Health Check
    print("\n1. Testando Health Check...")
    if not test_health():
        print("❌ API não está respondendo!")
        return
    
    # Teste 2: Listar Modelos
    print("\n2. Testando Lista de Modelos...")
    test_models()
    
    # Teste 3: Chat simples
    print("\n3. Testando Chat...")
    test_chat("Olá! Como você está?")
    
    # Teste 4: Chat mais complexo
    print("\n4. Testando Chat Complexo...")
    test_chat("Explique brevemente o que é inteligência artificial.")
    
    print("\n✅ Testes concluídos!")

if __name__ == "__main__":
    main()
