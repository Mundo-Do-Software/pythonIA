#!/usr/bin/env python3
"""
Teste rápido do modelo exportado
"""

import sys
from pathlib import Path

# Adicionar path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.fine_tuning.real_fine_tuning import SimplifiedFineTuner

def test_exported_model():
    """Testar modelo exportado"""
    print("🧪 Testando Modelo Exportado")
    print("=" * 40)
    
    # Encontrar modelo exportado (ajustar path para raiz do projeto)
    project_root = Path(__file__).parent.parent.parent
    exported_dir = project_root / "exported_models"
    
    if not exported_dir.exists():
        print("❌ Pasta exported_models não encontrada")
        return
    
    # Procurar arquivo pickle
    pickle_files = list(exported_dir.glob("fine_tuned_model_pickle_*.pkl"))
    
    if not pickle_files:
        print("❌ Nenhum modelo pickle exportado encontrado")
        return
    
    model_file = pickle_files[0]
    print(f"📂 Testando: {model_file.name}")
    
    try:
        # Carregar modelo
        tuner = SimplifiedFineTuner()
        success = tuner.load_model(str(model_file))
        
        if not success:
            print("❌ Falha ao carregar modelo")
            return
        
        print("✅ Modelo carregado com sucesso!")
        
        # Fazer alguns testes
        test_queries = [
            "Como resolver problema técnico?",
            "Preciso de ajuda médica",
            "Como cancelar pedido?",
            "Qual o preço do serviço?"
        ]
        
        print(f"\n🧪 Testando predições:")
        
        for query in test_queries:
            results = tuner.predict(query, top_k=2)
            
            if results:
                best = results[0]
                confidence = best['confidence'] * 100
                
                print(f"\n❓ {query}")
                print(f"   🎯 [{best['domain']}] ({confidence:.1f}%)")
                print(f"   🤖 {best['response'][:60]}...")
            else:
                print(f"\n❓ {query}")
                print(f"   ❌ Nenhuma predição")
        
        print(f"\n✅ Modelo exportado funcionando corretamente!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_exported_model()
