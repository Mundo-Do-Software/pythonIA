#!/usr/bin/env python3
"""
Teste rápido do fine-tuning
"""

import json
from pathlib import Path

def quick_test():
    """Teste rápido para verificar se funciona"""
    print("🧪 Teste Rápido do Fine-Tuning")
    print("=" * 40)
    
    # Verificar datasets
    training_dir = Path("training_data")
    
    if not training_dir.exists():
        print("❌ Pasta training_data não encontrada")
        return
    
    json_files = list(training_dir.glob("*.json"))
    print(f"📁 Encontrados {len(json_files)} arquivos JSON")
    
    total_conversations = 0
    domains = set()
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, dict) and 'conversations' in data:
                conversations = data['conversations']
                total_conversations += len(conversations)
                
                domain = data.get('metadata', {}).get('domain', 'unknown')
                domains.add(domain)
                
                print(f"✅ {json_file.name}: {len(conversations)} conversas, domínio: {domain}")
                
                # Mostrar exemplo
                if conversations:
                    example = conversations[0]
                    print(f"   📝 Exemplo: {example['input'][:50]}... → {example['output'][:50]}...")
                    
        except Exception as e:
            print(f"❌ Erro em {json_file}: {e}")
    
    print(f"\n📊 Resumo:")
    print(f"   💬 Total de conversas: {total_conversations}")
    print(f"   🏷️  Domínios únicos: {len(domains)}")
    print(f"   📂 Arquivos válidos: {len(json_files)}")
    
    if total_conversations > 0:
        print(f"\n✅ Dados prontos para fine-tuning!")
        print(f"💡 Execute: python scripts\\real_fine_tuning.py")
    else:
        print(f"\n⚠️  Nenhuma conversa encontrada")

if __name__ == "__main__":
    quick_test()
