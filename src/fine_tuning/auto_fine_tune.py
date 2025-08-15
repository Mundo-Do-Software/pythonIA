#!/usr/bin/env python3
"""
Script para fine-tuning automático baseado no cache Redis
Coleta dados reais de uso e treina adaptadores LoRA
"""

import asyncio
import json
import redis.asyncio as redis
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging
from pathlib import Path

# Importar o trainer
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
# from fine_tuning.lora_trainer import LoRAFineTuner, DomainSpecificTrainer
# Temporariamente comentado até implementarmos os trainers LoRA

class AutoFineTuner:
    """
    Sistema de fine-tuning automático que aprende do uso real
    Coleta dados do cache Redis e treina adaptadores específicos
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        # self.fine_tuner = LoRAFineTuner()
        # self.domain_trainer = DomainSpecificTrainer()
        # Temporariamente comentado até implementarmos os trainers LoRA
        
    async def collect_cache_data(self, days_back: int = 7) -> List[Dict]:
        """
        Coletar dados de conversas do cache Redis
        
        Args:
            days_back: Quantos dias atrás buscar dados
            
        Returns:
            Lista de conversas para treinamento
        """
        redis_client = redis.from_url(self.redis_url, decode_responses=True)
        training_data = []
        
        try:
            # Buscar todas as chaves de cache
            cache_keys = await redis_client.keys("cache:*")
            
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            for key in cache_keys:
                try:
                    cache_data = await redis_client.get(key)
                    if cache_data:
                        data = json.loads(cache_data)
                        
                        # Verificar se tem timestamp e está no período
                        if 'timestamp' in data:
                            timestamp = datetime.fromisoformat(data['timestamp'])
                            if timestamp > cutoff_date:
                                # Extrair pergunta original do cache key
                                query = key.replace("cache:", "").replace("_", " ")
                                
                                training_entry = {
                                    "input": query,
                                    "output": data.get('response', {}).get('choices', [{}])[0].get('message', {}).get('content', ''),
                                    "timestamp": data['timestamp'],
                                    "similarity_used": data.get('similarity', 0)
                                }
                                
                                # Só incluir se tem conteúdo válido
                                if training_entry["input"] and training_entry["output"]:
                                    training_data.append(training_entry)
                                    
                except json.JSONDecodeError:
                    continue
                    
        except Exception as e:
            logging.error(f"Erro ao coletar dados do cache: {e}")
        finally:
            await redis_client.close()
            
        return training_data
    
    def categorize_conversations(self, conversations: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Categorizar conversas por domínio usando keywords
        
        Args:
            conversations: Lista de conversas
            
        Returns:
            Dict com conversas categorizadas por domínio
        """
        categories = {
            "technical": [],
            "support": [],
            "legal": [],
            "general": []
        }
        
        # Keywords para classificação
        keywords = {
            "technical": ["api", "código", "programação", "docker", "redis", "ollama", "erro", "debug"],
            "support": ["login", "senha", "acesso", "conta", "problema", "ajuda", "como fazer"],
            "legal": ["contrato", "lei", "jurídico", "legal", "direito", "processo", "advogado"]
        }
        
        for conv in conversations:
            input_lower = conv["input"].lower()
            output_lower = conv["output"].lower()
            
            categorized = False
            
            # Classificar por keywords
            for category, kws in keywords.items():
                if any(kw in input_lower or kw in output_lower for kw in kws):
                    categories[category].append(conv)
                    categorized = True
                    break
            
            # Se não foi categorizado, vai para general
            if not categorized:
                categories["general"].append(conv)
                
        return categories
    
    async def auto_train_domains(self, min_examples_per_domain: int = 50):
        """
        Treinar automaticamente adaptadores para cada domínio
        
        Args:
            min_examples_per_domain: Mínimo de exemplos para treinar um domínio
        """
        logging.info("Iniciando fine-tuning automático...")
        
        # 1. Coletar dados do cache
        all_conversations = await self.collect_cache_data(days_back=30)
        logging.info(f"Coletadas {len(all_conversations)} conversas do cache")
        
        if len(all_conversations) < 10:
            logging.warning("Poucos dados disponíveis para fine-tuning")
            return
        
        # 2. Categorizar por domínio
        categorized = self.categorize_conversations(all_conversations)
        
        # 3. Treinar adaptador para cada domínio com dados suficientes
        trained_adapters = []
        
        for domain, conversations in categorized.items():
            if len(conversations) >= min_examples_per_domain:
                logging.info(f"Treinando domínio '{domain}' com {len(conversations)} exemplos")
                
                try:
                    if domain == "technical":
                        adapter_path = self.domain_trainer.train_technical_docs(conversations)
                    elif domain == "support":
                        adapter_path = self.domain_trainer.train_customer_support(conversations)
                    elif domain == "legal":
                        adapter_path = self.domain_trainer.train_portuguese_legal(conversations)
                    else:  # general
                        dataset_path = self.fine_tuner.prepare_dataset(conversations)
                        adapter_path = self.fine_tuner.train_lora_adapter(
                            dataset_path, f"general_{datetime.now().strftime('%Y%m%d')}", domain
                        )
                    
                    trained_adapters.append({
                        "domain": domain,
                        "adapter_path": adapter_path,
                        "examples_count": len(conversations),
                        "trained_at": datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    logging.error(f"Erro ao treinar domínio {domain}: {e}")
            else:
                logging.info(f"Domínio '{domain}' tem apenas {len(conversations)} exemplos (mínimo: {min_examples_per_domain})")
        
        # 4. Salvar relatório de treinamento
        report_path = Path("training_data") / f"training_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump({
                "trained_adapters": trained_adapters,
                "total_conversations": len(all_conversations),
                "categorization": {k: len(v) for k, v in categorized.items()},
                "training_date": datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Fine-tuning concluído! Relatório salvo: {report_path}")
        return trained_adapters

    def schedule_periodic_training(self, interval_days: int = 7):
        """
        Agendar treinamento periódico
        
        Args:
            interval_days: Intervalo em dias para re-treinar
        """
        # Implementar agendamento com scheduler (ex: APScheduler)
        pass


async def main():
    """Exemplo de uso do sistema de fine-tuning automático"""
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Inicializar auto fine-tuner
    auto_trainer = AutoFineTuner()
    
    # Executar treinamento automático
    try:
        trained_adapters = await auto_trainer.auto_train_domains(min_examples_per_domain=20)
        
        if trained_adapters:
            print("\n🎉 Fine-tuning Concluído!")
            print("Adaptadores treinados:")
            for adapter in trained_adapters:
                print(f"  • {adapter['domain']}: {adapter['examples_count']} exemplos")
        else:
            print("ℹ️  Nenhum adaptador foi treinado (dados insuficientes)")
            
    except Exception as e:
        logging.error(f"Erro no fine-tuning automático: {e}")


if __name__ == "__main__":
    asyncio.run(main())
