#!/usr/bin/env python3
"""
Verificador de Datasets Criados
Mostra resumo dos datasets personalizados
"""

import json
import csv
from pathlib import Path
from datetime import datetime

def analyze_datasets():
    """Analisa todos os datasets na pasta training_data"""
    training_dir = Path("training_data")
    
    if not training_dir.exists():
        print("❌ Pasta training_data não encontrada")
        return
    
    print("📊 Análise dos Datasets Personalizados")
    print("=" * 50)
    
    total_files = 0
    total_conversations = 0
    datasets_by_format = {"json": 0, "csv": 0, "jsonl": 0}
    
    # Listar todos os arquivos
    for file_path in training_dir.glob("*"):
        if file_path.suffix in ['.json', '.csv', '.jsonl']:
            total_files += 1
            file_conversations = 0
            
            print(f"\n📄 {file_path.name}")
            print(f"   📁 Tamanho: {file_path.stat().st_size} bytes")
            print(f"   📅 Criado: {datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Analisar conteúdo por formato
            try:
                if file_path.suffix == '.json':
                    datasets_by_format["json"] += 1
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    if isinstance(data, dict) and 'conversations' in data:
                        file_conversations = len(data['conversations'])
                        domain = data.get('metadata', {}).get('domain', 'unknown')
                        print(f"   🏷️  Domínio: {domain}")
                        print(f"   💬 Conversas: {file_conversations}")
                        
                        # Mostrar exemplo
                        if data['conversations']:
                            example = data['conversations'][0]
                            print(f"   📝 Exemplo:")
                            print(f"      👤 Input: {example['input'][:50]}...")
                            print(f"      🤖 Output: {example['output'][:50]}...")
                    
                elif file_path.suffix == '.csv':
                    datasets_by_format["csv"] += 1
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        rows = list(reader)
                        file_conversations = len(rows)
                        print(f"   💬 Linhas: {file_conversations}")
                        
                        if rows:
                            example = rows[0]
                            print(f"   📝 Exemplo:")
                            print(f"      👤 Input: {example.get('input', 'N/A')[:50]}...")
                            print(f"      🤖 Output: {example.get('output', 'N/A')[:50]}...")
                
                elif file_path.suffix == '.jsonl':
                    datasets_by_format["jsonl"] += 1
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        file_conversations = len([l for l in lines if l.strip()])
                        print(f"   💬 Linhas: {file_conversations}")
                
                total_conversations += file_conversations
                
            except Exception as e:
                print(f"   ⚠️  Erro ao analisar: {e}")
    
    # Resumo final
    print(f"\n🎯 Resumo Geral:")
    print(f"   📁 Total de arquivos: {total_files}")
    print(f"   💬 Total de conversas: {total_conversations}")
    print(f"   📊 Por formato:")
    for fmt, count in datasets_by_format.items():
        if count > 0:
            print(f"      • {fmt.upper()}: {count} arquivo(s)")
    
    if total_conversations > 0:
        print(f"\n✅ Datasets prontos para fine-tuning!")
        print(f"💡 Próximo passo: python scripts\\hybrid_fine_tuning.py")
    else:
        print(f"\n⚠️  Nenhuma conversa encontrada nos datasets")

if __name__ == "__main__":
    analyze_datasets()
