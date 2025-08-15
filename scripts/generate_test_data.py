#!/usr/bin/env python3
"""
Script para gerar dados de teste variados para o sistema de fine-tuning
"""

import requests
import json
import time

# URL da API
API_URL = "http://localhost:5000/v1/chat/completions"

# Dados de teste variados para diferentes domínios
test_queries = [
    # Programação
    {"content": "Como criar uma função em Python?", "domain": "programming"},
    {"content": "Qual a diferença entre list e tuple?", "domain": "programming"},
    {"content": "Como fazer um loop em JavaScript?", "domain": "programming"},
    
    # Culinária
    {"content": "Como fazer uma torta de maçã?", "domain": "cooking"},
    {"content": "Receita de bolo de chocolate", "domain": "cooking"},
    {"content": "Ingredientes para lasanha", "domain": "cooking"},
    
    # Tecnologia
    {"content": "O que é inteligência artificial?", "domain": "technology"},
    {"content": "Como funciona o machine learning?", "domain": "technology"},
    {"content": "Diferença entre AI e ML", "domain": "technology"},
    
    # Negócios
    {"content": "Como criar um plano de negócios?", "domain": "business"},
    {"content": "Estratégias de marketing digital", "domain": "business"},
    {"content": "Como aumentar vendas online?", "domain": "business"},
    
    # Educação
    {"content": "Métodos de estudo eficazes", "domain": "education"},
    {"content": "Como memorizar melhor?", "domain": "education"},
    {"content": "Técnicas de concentração", "domain": "education"},
]

def make_api_call(content):
    """Faz uma chamada para a API"""
    payload = {
        "model": "auto",
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ]
    }
    
    try:
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=120  # 2 minutos
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"Erro na requisição: {e}")
        return None

def main():
    """Função principal"""
    print("🚀 Iniciando geração de dados de teste...")
    print(f"📊 Total de consultas: {len(test_queries)}")
    
    successful_calls = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[{i}/{len(test_queries)}] Testando: {query['content'][:50]}...")
        
        result = make_api_call(query['content'])
        
        if result:
            successful_calls += 1
            print(f"✅ Sucesso! Domínio: {query['domain']}")
            # print(f"Resposta: {result['choices'][0]['message']['content'][:100]}...")
        else:
            print("❌ Falhou")
        
        # Pausa pequena entre requisições
        time.sleep(1)
    
    print(f"\n🎉 Processo concluído!")
    print(f"✅ Sucessos: {successful_calls}/{len(test_queries)}")
    print(f"📊 Taxa de sucesso: {(successful_calls/len(test_queries)*100):.1f}%")

if __name__ == "__main__":
    main()
