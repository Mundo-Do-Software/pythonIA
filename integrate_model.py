#!/usr/bin/env python3
"""
Script para integrar modelo fine-tuned na API
Atualiza a API para usar o modelo treinado
"""

import sys
from pathlib import Path
import shutil
import json

def integrate_fine_tuned_model():
    """Integrar o modelo fine-tuned na API"""
    print("🔗 Integrando Modelo Fine-Tuned na API")
    print("=" * 50)
    
    # Encontrar o modelo mais recente
    models_dir = Path("models")
    exported_dir = Path("exported_models")
    
    # Procurar o modelo mais recente
    model_files = list(models_dir.glob("fine_tuned_model_*.pkl"))
    
    if not model_files:
        print("❌ Nenhum modelo fine-tuned encontrado!")
        return False
    
    # Pegar o mais recente
    latest_model = max(model_files, key=lambda x: x.stat().st_mtime)
    print(f"📂 Modelo encontrado: {latest_model.name}")
    
    # Copiar para o diretório src para uso pela API
    src_dir = Path("src")
    target_path = src_dir / "current_fine_tuned_model.pkl"
    
    shutil.copy2(latest_model, target_path)
    print(f"✅ Modelo copiado para: {target_path}")
    
    # Criar arquivo de configuração
    config = {
        "fine_tuned_model": {
            "enabled": True,
            "model_path": str(target_path),
            "original_file": str(latest_model),
            "integrated_at": Path(latest_model).stat().st_mtime
        }
    }
    
    config_path = src_dir / "fine_tuning_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Configuração salva: {config_path}")
    
    # Mostrar próximos passos
    print(f"\n🚀 Próximos passos:")
    print(f"   1. Reiniciar API: docker-compose restart llm-api")
    print(f"   2. Aguardar inicialização (30-60s)")
    print(f"   3. Testar no Postman: POST http://localhost:5000/chat")
    
    return True

if __name__ == "__main__":
    success = integrate_fine_tuned_model()
    
    if success:
        print(f"\n🎉 Integração concluída!")
        print(f"💡 A API agora usará o modelo fine-tuned para respostas especializadas")
    else:
        print(f"\n❌ Falha na integração")
