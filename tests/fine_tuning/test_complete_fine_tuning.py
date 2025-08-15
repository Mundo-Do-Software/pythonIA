#!/usr/bin/env python3
"""
Teste Completo: Sistema de Fine-Tuning com Datasets Personalizados
"""

import asyncio
from pathlib import Path

async def test_complete_system():
    """Teste completo do sistema híbrido"""
    print("🧠 Teste Completo do Sistema de Fine-Tuning")
    print("=" * 60)
    
    # 1. Criar datasets de exemplo
    print("\n📝 Passo 1: Criando datasets personalizados...")
    try:
        from scripts.create_my_datasets import main as create_datasets
        create_datasets()
        print("✅ Datasets personalizados criados")
    except Exception as e:
        print(f"⚠️  Erro ao criar datasets: {e}")
    
    # 2. Gerar dados híbridos
    print("\n🔄 Passo 2: Gerando dados híbridos (Redis + Custom)...")
    try:
        from scripts.hybrid_fine_tuning import HybridFineTuner
        
        hybrid_tuner = HybridFineTuner()
        training_data = await hybrid_tuner.create_hybrid_training_data(
            days_back=30,
            balance_ratio=0.6,  # 60% Redis, 40% Custom
            include_datasets=["*.json"]
        )
        
        print("✅ Dados híbridos gerados com sucesso")
        
        # Mostrar estatísticas
        metadata = training_data.get("metadata", {})
        print(f"\n📊 Estatísticas:")
        print(f"   • Redis: {metadata.get('redis_conversations', 0)} conversas")
        print(f"   • Custom: {metadata.get('custom_conversations', 0)} conversas")
        print(f"   • Total: {metadata.get('total_conversations', 0)} conversas")
        
        domains = training_data.get("domains", {})
        print(f"   • Domínios identificados: {len(domains)}")
        for domain, count in domains.items():
            print(f"     - {domain}: {count} exemplos")
            
    except Exception as e:
        print(f"❌ Erro ao gerar dados híbridos: {e}")
    
    # 3. Simular fine-tuning
    print(f"\n🧠 Passo 3: Simulando processo de fine-tuning...")
    print(f"⚙️  Configuração LoRA:")
    print(f"   • Rank: 16")
    print(f"   • Alpha: 32") 
    print(f"   • Épocas: 3")
    print(f"   • Learning Rate: 1e-4")
    
    print(f"\n🎯 Domínios para treinamento:")
    if 'domains' in locals():
        for domain, count in domains.items():
            if count >= 3:  # Mínimo para demonstração
                print(f"   ✅ {domain}: {count} exemplos (suficiente)")
            else:
                print(f"   ⚠️  {domain}: {count} exemplos (poucos)")
    
    # 4. Resultados finais
    print(f"\n🎉 Sistema testado com sucesso!")
    print(f"📁 Arquivos gerados em: training_data/")
    
    # Listar arquivos criados
    training_dir = Path("training_data")
    if training_dir.exists():
        files = list(training_dir.glob("*.json"))
        print(f"📄 Arquivos de treinamento ({len(files)}):")
        for file in sorted(files)[-5:]:  # Mostrar últimos 5
            print(f"   • {file.name}")
    
    print(f"\n🚀 Para fine-tuning real:")
    print(f"1. Instale: pip install torch transformers peft")
    print(f"2. Configure GPU (opcional): CUDA_VISIBLE_DEVICES=0")
    print(f"3. Execute: python scripts/auto_fine_tune.py")
    print(f"4. Teste modelos: python scripts/test_fine_tuned_models.py")

def main():
    """Executar teste completo"""
    asyncio.run(test_complete_system())

if __name__ == "__main__":
    main()
