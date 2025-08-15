#!/usr/bin/env python3
"""
Test different prompting strategies with deepseek-coder
"""
import requests
import json

def test_prompting_strategies():
    print("Testando estratégias de prompt com deepseek-coder:1.3b...")
    
    # Diferentes estratégias de prompt
    prompts = [
        # Estratégia 1: Simples
        "Olá! Como você está?",
        
        # Estratégia 2: Contexto técnico
        "Como desenvolvedor, explique como funciona um motor de combustão",
        
        # Estratégia 3: Role-playing suave
        "Atue como assistente técnico e explique motores de moto",
        
        # Estratégia 4: Pergunta direta sem role-play
        "Quais são as partes principais de um motor de motocicleta?",
        
        # Estratégia 5: Contextualizado como educação
        "Para fins educacionais, liste os componentes básicos de um motor",
        
        # Estratégia 6: Código relacionado
        "Crie um código Python que liste as partes de um motor de moto",
        
        # Estratégia 7: Muito simples
        "Diga: Sistema funcionando!"
    ]
    
    model = 'deepseek-coder:1.3b'
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n{'='*60}")
        print(f"TESTE {i}: {prompt}")
        print(f"{'='*60}")
        
        payload = {
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 150,
            'temperature': 0.3  # Menos criatividade, mais determinístico
        }
        
        try:
            response = requests.post('http://localhost:5000/v1/chat/completions', json=payload, timeout=45)
            
            if response.status_code == 200:
                data = response.json()
                if 'choices' in data and len(data['choices']) > 0:
                    content = data['choices'][0]['message']['content']
                    print(f"✅ RESPOSTA:\n{content}\n")
                else:
                    print("❌ No choices in response")
            else:
                print(f"❌ ERRO {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")
            
        print("-" * 60)

if __name__ == "__main__":
    test_prompting_strategies()
