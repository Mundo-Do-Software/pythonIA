#!/usr/bin/env python3
"""
Script para pré-aquecer os modelos e otimizar performance
"""
import requests
import time
import json

OLLAMA_URL = "http://localhost:11434"

def warm_up_model(model_name: str):
    """Pré-aquece um modelo específico"""
    print(f"🔥 Aquecendo modelo: {model_name}")
    
    warm_up_payload = {
        "model": model_name,
        "prompt": "Hello",
        "stream": False,
        "options": {
            "num_predict": 1,
            "temperature": 0.1
        }
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=warm_up_payload, timeout=60)
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            print(f"✅ {model_name} aquecido em {elapsed:.1f}s")
            return True
        else:
            print(f"❌ Erro ao aquecer {model_name}: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exceção ao aquecer {model_name}: {e}")
        return False

def optimize_models():
    """Otimiza configurações dos modelos"""
    
    models_to_warm = ["mistral:latest", "llama3.2:3b"]
    
    print("🚀 INICIANDO OTIMIZAÇÃO DE PERFORMANCE")
    print("=" * 50)
    
    for model in models_to_warm:
        print(f"\n🔥 Processando {model}...")
        
        # Verificar se modelo existe
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
            if response.status_code == 200:
                available_models = [m["name"] for m in response.json().get("models", [])]
                if model in available_models:
                    warm_up_model(model)
                else:
                    print(f"⚠️  Modelo {model} não encontrado")
            
        except Exception as e:
            print(f"❌ Erro ao verificar modelos: {e}")
    
    print(f"\n✅ Otimização concluída!")
    print("💡 Dica: Execute este script após reiniciar o Docker para melhor performance")

if __name__ == "__main__":
    optimize_models()
