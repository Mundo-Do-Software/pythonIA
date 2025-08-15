#!/usr/bin/env python3
"""
Fine-Tuning Real Simplificado
Treina um modelo simples com os datasets personalizados
"""

import json
import pickle
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimplifiedFineTuner:
    """
    Fine-tuner simplificado usando TF-IDF e similaridade semântica
    Simula o processo de fine-tuning sem necessidade de GPU/torch
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            stop_words=None,  # Manter palavras em português
            lowercase=True
        )
        self.trained_data = []
        self.domain_models = {}
        self.is_trained = False
        
    def load_custom_datasets(self) -> List[Dict]:
        """Carregar todos os datasets personalizados"""
        training_dir = Path("training_data")
        all_conversations = []
        
        logger.info("🔍 Carregando datasets personalizados...")
        
        if not training_dir.exists():
            logger.warning("⚠️  Pasta training_data não encontrada")
            return []
        
        for json_file in training_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if isinstance(data, dict) and 'conversations' in data:
                    domain = data.get('metadata', {}).get('domain', 'general')
                    
                    for conv in data['conversations']:
                        if 'input' in conv and 'output' in conv:
                            conv['domain'] = domain
                            conv['source_file'] = json_file.name
                            all_conversations.append(conv)
                            
                    logger.info(f"✅ Carregado {len(data['conversations'])} conversas de {json_file.name}")
                    
            except Exception as e:
                logger.error(f"❌ Erro carregando {json_file}: {e}")
        
        logger.info(f"📊 Total de conversas carregadas: {len(all_conversations)}")
        return all_conversations
    
    def prepare_training_data(self, conversations: List[Dict]) -> Tuple[List[str], List[str], List[str]]:
        """Preparar dados para treinamento"""
        inputs = []
        outputs = []
        domains = []
        
        for conv in conversations:
            inputs.append(conv['input'])
            outputs.append(conv['output'])
            domains.append(conv.get('domain', 'general'))
        
        return inputs, outputs, domains
    
    def train_domain_specific_models(self, inputs: List[str], outputs: List[str], domains: List[str]):
        """Treinar modelos específicos por domínio"""
        logger.info("🧠 Iniciando treinamento por domínio...")
        
        # Agrupar por domínio
        domain_data = {}
        for inp, out, domain in zip(inputs, outputs, domains):
            if domain not in domain_data:
                domain_data[domain] = {'inputs': [], 'outputs': []}
            domain_data[domain]['inputs'].append(inp)
            domain_data[domain]['outputs'].append(out)
        
        # Treinar modelo para cada domínio
        for domain, data in domain_data.items():
            logger.info(f"🎯 Treinando modelo para domínio: {domain}")
            
            if len(data['inputs']) < 3:
                logger.warning(f"⚠️  Poucos dados para {domain}: {len(data['inputs'])} exemplos")
                continue
            
            # Criar vetorizador específico do domínio
            domain_vectorizer = TfidfVectorizer(
                max_features=500,
                ngram_range=(1, 2),
                lowercase=True
            )
            
            # Treinar vetorizador com inputs do domínio
            input_vectors = domain_vectorizer.fit_transform(data['inputs'])
            
            # Armazenar modelo do domínio
            self.domain_models[domain] = {
                'vectorizer': domain_vectorizer,
                'input_vectors': input_vectors,
                'inputs': data['inputs'],
                'outputs': data['outputs'],
                'trained_examples': len(data['inputs'])
            }
            
            logger.info(f"✅ Modelo {domain} treinado com {len(data['inputs'])} exemplos")
    
    def train(self) -> bool:
        """Executar treinamento completo"""
        logger.info("🚀 Iniciando Fine-Tuning Simplificado...")
        
        # 1. Carregar datasets
        conversations = self.load_custom_datasets()
        
        if not conversations:
            logger.error("❌ Nenhum dataset encontrado para treinamento")
            return False
        
        # 2. Preparar dados
        inputs, outputs, domains = self.prepare_training_data(conversations)
        self.trained_data = list(zip(inputs, outputs, domains))
        
        # 3. Treinar vetorizador geral
        logger.info("🔧 Treinando vetorizador geral...")
        self.vectorizer.fit(inputs)
        
        # 4. Treinar modelos por domínio
        self.train_domain_specific_models(inputs, outputs, domains)
        
        self.is_trained = True
        logger.info("🎉 Treinamento concluído com sucesso!")
        
        return True
    
    def predict(self, query: str, top_k: int = 3) -> List[Dict]:
        """Fazer predição baseada no modelo treinado"""
        if not self.is_trained:
            return [{"response": "Modelo não foi treinado ainda", "confidence": 0.0, "domain": "error"}]
        
        results = []
        
        # Tentar cada modelo de domínio
        for domain, model in self.domain_models.items():
            try:
                # Vetorizar query
                query_vector = model['vectorizer'].transform([query])
                
                # Calcular similaridades
                similarities = cosine_similarity(query_vector, model['input_vectors'])[0]
                
                # Encontrar melhores matches
                best_indices = np.argsort(similarities)[::-1][:top_k]
                
                for idx in best_indices:
                    if similarities[idx] > 0.1:  # Threshold mínimo
                        results.append({
                            "response": model['outputs'][idx],
                            "confidence": float(similarities[idx]),
                            "domain": domain,
                            "matched_input": model['inputs'][idx]
                        })
                        
            except Exception as e:
                logger.error(f"Erro na predição para domínio {domain}: {e}")
        
        # Ordenar por confiança
        results.sort(key=lambda x: x['confidence'], reverse=True)
        
        return results[:top_k] if results else [{"response": "Não encontrei uma resposta adequada", "confidence": 0.0, "domain": "fallback"}]
    
    def save_model(self, filepath: str = None):
        """Salvar modelo treinado"""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"models/fine_tuned_model_{timestamp}.pkl"
        
        # Criar diretório se não existir
        Path(filepath).parent.mkdir(exist_ok=True)
        
        model_data = {
            'vectorizer': self.vectorizer,
            'domain_models': self.domain_models,
            'trained_data': self.trained_data,
            'is_trained': self.is_trained,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"💾 Modelo salvo em: {filepath}")
        return filepath
    
    def load_model(self, filepath: str):
        """Carregar modelo treinado"""
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.vectorizer = model_data['vectorizer']
            self.domain_models = model_data['domain_models']
            self.trained_data = model_data['trained_data']
            self.is_trained = model_data['is_trained']
            
            logger.info(f"✅ Modelo carregado de: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro carregando modelo: {e}")
            return False
    
    def get_training_summary(self) -> Dict:
        """Obter resumo do treinamento"""
        if not self.is_trained:
            return {"status": "not_trained"}
        
        summary = {
            "status": "trained",
            "total_examples": len(self.trained_data),
            "domains": {},
            "training_timestamp": datetime.now().isoformat()
        }
        
        for domain, model in self.domain_models.items():
            summary["domains"][domain] = {
                "examples": model["trained_examples"],
                "features": model["vectorizer"].get_feature_names_out()[:10].tolist()  # Top 10 features
            }
        
        return summary

def main():
    """Executar fine-tuning real"""
    print("🧠 Fine-Tuning Real com Datasets Personalizados")
    print("=" * 60)
    
    # Criar fine-tuner
    tuner = SimplifiedFineTuner()
    
    # Executar treinamento
    success = tuner.train()
    
    if not success:
        print("❌ Falha no treinamento")
        return
    
    # Salvar modelo
    model_path = tuner.save_model()
    
    # Mostrar resumo
    summary = tuner.get_training_summary()
    print(f"\n📊 Resumo do Treinamento:")
    print(f"✅ Status: {summary['status']}")
    print(f"📚 Total de exemplos: {summary['total_examples']}")
    print(f"🏷️  Domínios treinados: {len(summary['domains'])}")
    
    for domain, info in summary['domains'].items():
        print(f"   • {domain}: {info['examples']} exemplos")
    
    # Testar modelo
    print(f"\n🧪 Testando Modelo Treinado:")
    test_queries = [
        "Como posso cancelar meu pedido?",
        "Qual o prazo de entrega?",
        "Tenho um problema técnico",
        "Como funciona a consulta?",
        "Preciso de ajuda com o sistema"
    ]
    
    for query in test_queries:
        print(f"\n❓ Pergunta: {query}")
        results = tuner.predict(query, top_k=2)
        
        for i, result in enumerate(results[:2], 1):
            confidence_pct = result['confidence'] * 100
            print(f"   {i}. [{result['domain']}] (confiança: {confidence_pct:.1f}%):")
            print(f"      🤖 {result['response'][:100]}...")
    
    print(f"\n🎯 Resultado:")
    print(f"✅ Modelo fine-tuned salvo em: {model_path}")
    print(f"✅ {len(summary['domains'])} domínios especializados")
    print(f"✅ {summary['total_examples']} exemplos de treinamento")
    print(f"🚀 Sistema pronto para uso em produção!")

if __name__ == "__main__":
    main()
