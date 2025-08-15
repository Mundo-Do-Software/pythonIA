#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste super simples e rapido para validar que a API funciona
"""

import requests
import time

def test_api_basica():
    """Teste minimo da API"""
    print("Testando API basica...")
    
    try:
        # Teste 1: Health check
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✓ API respondendo")
        else:
            print(f"✗ API erro: {response.status_code}")
            return False
        
        # Teste 2: Chat simples com timeout baixo
        data = {
            "model": "mistral",
            "messages": [{"role": "user", "content": "Oi"}],
            "max_tokens": 10
        }
        
        start_time = time.time()
        response = requests.post("http://localhost:5000/v1/chat/completions", 
                               json=data, timeout=15)  # Timeout menor
        
        if response.status_code == 200:
            elapsed = time.time() - start_time
            result = response.json()
            message = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(f"✓ Chat funcionando ({elapsed:.1f}s)")
            print(f"  Resposta: {message[:50]}...")
            return True
        else:
            print(f"✗ Chat erro: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏱ Timeout - API demorou muito para responder")
        return False
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False

if __name__ == "__main__":
    print("TESTE SUPER RAPIDO DA API")
    print("=" * 30)
    
    success = test_api_basica()
    
    if success:
        print("\n✓ SUCESSO: API funcionando corretamente!")
    else:
        print("\n✗ FALHA: Verifique se os servicos estao rodando")
        print("  docker-compose -f docker-compose.ollama.yml up -d")
