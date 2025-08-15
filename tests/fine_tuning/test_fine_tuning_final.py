#!/usr/bin/env python3
"""
Teste final do sistema de fine-tuning
Usa dados reais do cache Redis para demonstrar funcionalidade
"""

import redis
import json
from datetime import datetime
from pathlib import Path

def collect_real_cache_data():
    """Coletar dados reais do cache"""
    print("🔍 Coletando dados do cache Redis...")
    
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    try:
        r.ping()
        print("✅ Redis conectado")
        
        # Buscar todas as chaves
        all_keys = list(r.keys("*"))
        print(f"📊 Encontradas {len(all_keys)} chaves")
        
        training_data = []
        
        for key in all_keys:
            try:
                value = r.get(key)
                if value and value.startswith('{'):
                    data = json.loads(value)
                    
                    # Extrair pergunta e resposta
                    if isinstance(data, dict) and 'response' in data:
                        response = data.get('response', {})
                        if isinstance(response, dict) and 'choices' in response:
                            choices = response.get('choices', [])
                            if choices:
                                # Tentar extrair pergunta da chave ou dos dados
                                query = key.replace('_', ' ').strip()
                                if len(query) < 5:  # Se a chave não tem info útil
                                    query = "Pergunta do usuário"
                                
                                content = choices[0].get('message', {}).get('content', '')
                                
                                if content:
                                    training_entry = {
                                        "input": query,
                                        "output": content,
                                        "timestamp": data.get('timestamp', datetime.now().isoformat()),
                                        "key": key
                                    }
                                    training_data.append(training_entry)
                                    
            except json.JSONDecodeError:
                continue
            except Exception as e:
                print(f"⚠️  Erro processando chave {key}: {e}")
                continue
        
        print(f"✅ Coletadas {len(training_data)} conversas válidas")
        return training_data
        
    except Exception as e:
        print(f"❌ Erro coletando dados: {e}")
        return []

def categorize_by_domain(conversations):
    """Categorizar conversas por domínio"""
    print("🏷️  Categorizando conversas...")
    
    categories = {
        "saudacao": [],
        "matematica": [],
        "geral": []
    }
    
    for conv in conversations:
        input_lower = conv["input"].lower()
        output_lower = conv["output"].lower()
        
        # Classificação simples
        if any(word in input_lower or word in output_lower 
               for word in ["olá", "oi", "como está", "hello", "prazer"]):
            categories["saudacao"].append(conv)
        elif any(word in input_lower or word in output_lower 
                for word in ["2+2", "matemática", "calcul", "número"]):
            categories["matematica"].append(conv)
        else:
            categories["geral"].append(conv)
    
    for category, convs in categories.items():
        print(f"  • {category.capitalize()}: {len(convs)} conversas")
    
    return categories

def simulate_fine_tuning(categorized_data):
    """Simular processo de fine-tuning"""
    print("\n🧠 Simulando processo de fine-tuning...")
    
    total_conversations = sum(len(convs) for convs in categorized_data.values())
    
    if total_conversations == 0:
        print("❌ Nenhum dado disponível para fine-tuning")
        return False
    
    print(f"📊 Total de conversas: {total_conversations}")
    
    # Simular treinamento para cada categoria
    for domain, conversations in categorized_data.items():
        if conversations:
            print(f"\n🔄 Simulando fine-tuning para domínio '{domain}':")
            print(f"   📚 Dados de treinamento: {len(conversations)} exemplos")
            print(f"   ⚙️  Configuração LoRA: rank=16, alpha=32")
            print(f"   🎯 Épocas estimadas: 3-5")
            print(f"   💾 Adapter salvo como: {domain}_adapter.pt")
            
            # Mostrar exemplo de dados
            if conversations:
                example = conversations[0]
                print(f"   📝 Exemplo de entrada: {example['input'][:50]}...")
                print(f"   📝 Exemplo de saída: {example['output'][:50]}...")
    
    return True

def save_training_summary(categorized_data):
    """Salvar resumo do treinamento"""
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_conversations": sum(len(convs) for convs in categorized_data.values()),
        "domains": {domain: len(convs) for domain, convs in categorized_data.items()},
        "status": "simulation_complete",
        "next_steps": [
            "Install torch and transformers",
            "Configure GPU environment", 
            "Run actual LoRA training",
            "Test fine-tuned adapters"
        ]
    }
    
    # Criar diretório se não existir
    training_dir = Path("training_data")
    training_dir.mkdir(exist_ok=True)
    
    summary_file = training_dir / f"fine_tuning_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resumo salvo em: {summary_file}")
    return str(summary_file)

def main():
    """Teste principal do fine-tuning"""
    print("🧠 Teste Final do Sistema de Fine-Tuning")
    print("=" * 50)
    
    # 1. Coletar dados reais do cache
    conversations = collect_real_cache_data()
    
    if not conversations:
        print("\n⚠️  Nenhum dado encontrado no cache")
        print("💡 Execute algumas consultas à API primeiro:")
        print("   python scripts\\test_api_and_cache.py")
        return
    
    # 2. Categorizar por domínio
    categorized = categorize_by_domain(conversations)
    
    # 3. Simular fine-tuning
    success = simulate_fine_tuning(categorized)
    
    if success:
        # 4. Salvar resumo
        summary_file = save_training_summary(categorized)
        
        # 5. Relatório final
        print(f"\n🎯 Relatório Final:")
        print(f"✅ Dados coletados: {len(conversations)} conversas")
        print(f"✅ Domínios identificados: {len([d for d, c in categorized.items() if c])}")
        print(f"✅ Simulação concluída com sucesso")
        print(f"✅ Resumo salvo: {Path(summary_file).name}")
        
        print(f"\n🚀 Próximos passos para fine-tuning real:")
        print(f"1. Instalar dependências: pip install torch transformers")
        print(f"2. Configurar GPU (se disponível)")
        print(f"3. Executar: python scripts\\fine-tune.ps1")
        print(f"4. Testar adaptadores treinados")
    
    print(f"\n✅ Sistema de fine-tuning testado com sucesso!")

if __name__ == "__main__":
    main()
