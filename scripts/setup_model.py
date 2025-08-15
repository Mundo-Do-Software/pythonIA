#!/usr/bin/env python3
"""
Script para baixar modelo Mistral no Ollama
"""
import requests
import json
import time

def download_model(model_name="mistral"):
    """Baixa um modelo no Ollama"""
    print(f"📥 Iniciando download do modelo: {model_name}")
    
    try:
        payload = {"name": model_name}
        
        response = requests.post(
            "http://localhost:11434/api/pull",
            json=payload,
            stream=True
        )
        
        if response.status_code == 200:
            print("✅ Download iniciado com sucesso!")
            
            # Acompanhar progresso
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        data = json.loads(line)
                        if "status" in data:
                            print(f"📊 Status: {data['status']}")
                        if "completed" in data and "total" in data:
                            progress = (data["completed"] / data["total"]) * 100
                            print(f"📈 Progresso: {progress:.1f}%")
                    except json.JSONDecodeError:
                        pass
            
            print("🎉 Download concluído!")
            return True
        else:
            print(f"❌ Erro no download: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def list_models():
    """Lista modelos disponíveis"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json()
            print("📋 Modelos disponíveis:")
            for model in models.get("models", []):
                print(f"   - {model['name']}")
            return models.get("models", [])
        else:
            print(f"❌ Erro ao listar modelos: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Erro: {e}")
        return []

def main():
    print("🚀 Configurador de Modelo Ollama")
    print("=" * 40)
    
    # Verificar modelos existentes
    print("\n1. Verificando modelos existentes...")
    models = list_models()
    
    if any("mistral" in model["name"] for model in models):
        print("✅ Mistral já está disponível!")
    else:
        print("⬇️ Mistral não encontrado, iniciando download...")
        download_model("mistral")
    
    print("\n2. Verificação final...")
    list_models()
    
    print("\n✅ Configuração concluída!")

if __name__ == "__main__":
    main()
