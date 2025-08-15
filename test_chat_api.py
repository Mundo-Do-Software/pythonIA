#!/usr/bin/env python3
"""
Test script for chat completion API
"""
import requests
import json

def test_chat_completion():
    print("Testando chat completion...")
    
    # Teste com diferentes modelos
    models_to_test = ['deepseek-coder:1.3b', 'deepseek-coder', 'deepseek', 'mistral:latest', 'llama3.2:3b']
    
    for model in models_to_test:
        print(f"\n--- Testando modelo: {model} ---")
        
        payload = {
            'model': model,
            'messages': [{'role': 'user', 'content': 'Diga apenas: Olá! Sistema funcionando!'}],
            'max_tokens': 50,
            'temperature': 0.7
        }
        
        try:
            response = requests.post('http://localhost:5000/v1/chat/completions', json=payload, timeout=30)
            print(f"Status Code: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {data}")
                if 'choices' in data and len(data['choices']) > 0:
                    print(f"Content: {data['choices'][0]['message']['content']}")
                else:
                    print("No choices in response")
            else:
                print(f"Error: {response.text}")
                
            # Para após o primeiro sucesso
            if response.status_code == 200 and 'choices' in response.json():
                break
                
        except Exception as e:
            print(f"Exception: {e}")
            continue

if __name__ == "__main__":
    test_chat_completion()
