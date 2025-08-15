#!/usr/bin/env python3
"""
Test script for chat completion API - Testing different models
"""
import requests
import json

def test_different_models():
    print("Testando diferentes modelos...")
    
    # Modelos disponíveis em ordem de preferência para conversação
    models_to_test = [
        'llama3.2:3b',      # Melhor para conversação geral
        'mistral:latest',   # Bom para conversação
        'deepseek-coder:1.3b'  # Especializado em código
    ]
    
    test_messages = [
        "Diga apenas: Olá! Sistema funcionando!",
        "Você é RICARDO, mecânico de motos experiente. Responda em português brasileiro com soluções práticas. Seja objetivo e conciso e poucas palavras",
        "Como funciona um motor de moto?"
    ]
    
    for model in models_to_test:
        print(f"\n{'='*50}")
        print(f"TESTANDO MODELO: {model}")
        print(f"{'='*50}")
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n--- Teste {i}: {message[:50]}... ---")
            
            payload = {
                'model': model,
                'messages': [{'role': 'user', 'content': message}],
                'max_tokens': 100,
                'temperature': 0.7
            }
            
            try:
                response = requests.post('http://localhost:5000/v1/chat/completions', json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    if 'choices' in data and len(data['choices']) > 0:
                        content = data['choices'][0]['message']['content']
                        print(f"✅ SUCESSO: {content[:200]}...")
                    else:
                        print("❌ No choices in response")
                else:
                    print(f"❌ ERRO {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"❌ EXCEPTION: {e}")
                break  # Se um modelo falha, tenta o próximo
                
            print("-" * 50)

if __name__ == "__main__":
    test_different_models()
