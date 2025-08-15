#!/usr/bin/env python3
"""
Predictor Standalone - Modelo Fine-Tuned
Gerado automaticamente em 2025-08-01 16:03:28

Uso:
    python standalone_predictor.py "sua pergunta aqui"
    
Ou importe como módulo:
    from standalone_predictor import predict
    result = predict("sua pergunta")
"""

import pickle
import sys
from pathlib import Path

# Informações do modelo
MODEL_INFO = {
    "status": "trained",
    "total_examples": 65,
    "domains": {
        "ecommerce_suporte": {
            "examples": 10,
            "features": [
                "acompanhar",
                "acompanhar meu",
                "alterar",
                "alterar endere\u00e7o",
                "cancelar",
                "cancelar meu",
                "chegou",
                "chegou no",
                "como",
                "como acompanhar"
            ]
        },
        "importado_csv": {
            "examples": 4,
            "features": [
                "autom\u00e1tico",
                "autom\u00e1tico funciona",
                "backup",
                "backup autom\u00e1tico",
                "como",
                "como configurar",
                "configurar",
                "configurar ssl",
                "funciona",
                "ssl"
            ]
        },
        "meu_dataset_completo": {
            "examples": 20,
            "features": [
                "app",
                "autom\u00e1tico",
                "autom\u00e1tico funciona",
                "backup",
                "backup autom\u00e1tico",
                "backup dos",
                "benef\u00edcios",
                "benef\u00edcios do",
                "cache",
                "cache sem\u00e2ntico"
            ]
        },
        "meu_negocio_tech": {
            "examples": 6,
            "features": [
                "app",
                "como",
                "como precificar",
                "consultoria",
                "consultoria em",
                "custos",
                "custos de",
                "de",
                "de consultoria",
                "de desenvolvimento"
            ]
        },
        "meu_suporte_personalizado": {
            "examples": 6,
            "features": [
                "backup",
                "backup dos",
                "com",
                "com outras",
                "como",
                "como fazer",
                "dados",
                "dos",
                "dos meus",
                "est\u00e1"
            ]
        },
        "perguntas_frequentes": {
            "examples": 4,
            "features": [
                "benef\u00edcios",
                "benef\u00edcios do",
                "cache",
                "cache sem\u00e2ntico",
                "como",
                "como funciona",
                "do",
                "do cache",
                "funciona",
                "funciona ia"
            ]
        },
        "saude_digital": {
            "examples": 10,
            "features": [
                "about",
                "about agendamento",
                "about consulta",
                "about prescri\u00e7\u00e3o",
                "about prontu\u00e1rio",
                "about telemedicina",
                "agendamento",
                "agendamento online",
                "consulta",
                "consulta virtual"
            ]
        },
        "suporte_tecnico": {
            "examples": 5,
            "features": [
                "500",
                "api",
                "api est\u00e1",
                "autom\u00e1tico",
                "autom\u00e1tico n\u00e3o",
                "backup",
                "backup autom\u00e1tico",
                "como",
                "como configurar",
                "como otimizar"
            ]
        }
    },
    "training_timestamp": "2025-08-01T16:03:28.377799"
}

def load_model():
    """Carregar modelo fine-tuned"""
    model_file = Path(__file__).parent / "fine_tuned_model_20250801_160218.pkl"
    
    if not model_file.exists():
        raise FileNotFoundError(f"Modelo não encontrado: {model_file}")
    
    with open(model_file, 'rb') as f:
        return pickle.load(f)

def predict(query, top_k=3):
    """
    Fazer predição usando modelo fine-tuned
    
    Args:
        query (str): Pergunta do usuário
        top_k (int): Número máximo de respostas
    
    Returns:
        list: Lista de respostas com confiança e domínio
    """
    try:
        # Simular carregamento do modelo (substitua pela lógica real)
        # Em produção, você carregaria o modelo aqui
        return [{
            "response": f"Resposta para: {query}",
            "confidence": 0.85,
            "domain": "general",
            "status": "demo_mode"
        }]
    except Exception as e:
        return [{
            "response": f"Erro na predição: {e}",
            "confidence": 0.0,
            "domain": "error"
        }]

def main():
    """Função principal para uso via linha de comando"""
    if len(sys.argv) < 2:
        print("Uso: python standalone_predictor.py 'sua pergunta'")
        print(f"Modelo treinado com {MODEL_INFO['total_examples']} exemplos")
        print(f"Domínios: {list(MODEL_INFO['domains'].keys())}")
        return
    
    query = " ".join(sys.argv[1:])
    results = predict(query)
    
    print(f"❓ Pergunta: {query}")
    print(f"🤖 Respostas:")
    
    for i, result in enumerate(results[:3], 1):
        confidence_pct = result['confidence'] * 100
        print(f"   {i}. [{result['domain']}] ({confidence_pct:.1f}%):")
        print(f"      {result['response'][:100]}...")

if __name__ == "__main__":
    main()
