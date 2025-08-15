#!/usr/bin/env python3
"""
Fine-Tuning Híbrido: Cache Redis + Datasets Personalizados
Combina dados reais de uso com datasets customizados
"""

import asyncio
import json
import redis.asyncio as redis
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

# Importar geradores
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.fine_tuning.dataset_generator import DatasetGenerator

class HybridFineTuner:
    """
    Sistema híbrido de fine-tuning que combina:
    1. Dados reais do cache Redis (uso real da API)
    2. Datasets personalizados criados pelo usuário
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.dataset_generator = DatasetGenerator()
        self.training_data_dir = Path("training_data")
        self.training_data_dir.mkdir(exist_ok=True)
        
    async def collect_redis_data(self, days_back: int = 7) -> List[Dict]:
        """Coletar dados reais do cache Redis"""
        print("🔄 Coletando dados do cache Redis...")
        
        redis_client = redis.from_url(self.redis_url, decode_responses=True)
        training_data = []
        
        try:
            # Buscar todas as chaves
            all_keys = await redis_client.keys("*")
            print(f"🗝️  Encontradas {len(all_keys)} chaves no Redis")
            
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            for key in all_keys:
                try:
                    value = await redis_client.get(key)
                    if value and value.startswith('{'):
                        data = json.loads(value)
                        
                        # Extrair conversas válidas
                        if isinstance(data, dict) and 'response' in data:
                            response = data.get('response', {})
                            if isinstance(response, dict) and 'choices' in response:
                                choices = response.get('choices', [])
                                if choices:
                                    # Tentar extrair pergunta
                                    query = key.replace('_', ' ').strip()
                                    if len(query) < 5:
                                        query = "Pergunta do usuário"
                                    
                                    content = choices[0].get('message', {}).get('content', '')
                                    
                                    if content:
                                        training_entry = {
                                            "input": query,
                                            "output": content,
                                            "source": "redis_cache",
                                            "timestamp": data.get('timestamp', datetime.now().isoformat()),
                                            "similarity_used": data.get('similarity', 0)
                                        }
                                        training_data.append(training_entry)
                                        
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    continue
            
            print(f"✅ Coletadas {len(training_data)} conversas do Redis")
            return training_data
            
        except Exception as e:
            print(f"❌ Erro ao coletar dados do Redis: {e}")
            return []
        finally:
            await redis_client.close()
    
    def load_custom_datasets(self, dataset_patterns: List[str] = ["*.json"]) -> List[Dict]:
        """Carregar datasets personalizados"""
        print("📂 Carregando datasets personalizados...")
        
        all_conversations = []
        
        for pattern in dataset_patterns:
            dataset_files = list(self.training_data_dir.glob(pattern))
            
            for file_path in dataset_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Extrair conversas baseado na estrutura
                    conversations = []
                    if isinstance(data, dict) and "conversations" in data:
                        conversations = data["conversations"]
                        domain = data.get("metadata", {}).get("domain", "unknown")
                    elif isinstance(data, list):
                        conversations = data
                        domain = "imported"
                    
                    # Adicionar metadados de fonte
                    for conv in conversations:
                        conv["source"] = "custom_dataset"
                        conv["dataset_file"] = file_path.name
                        conv["domain"] = conv.get("domain", domain)
                    
                    all_conversations.extend(conversations)
                    print(f"📥 {file_path.name}: {len(conversations)} conversas")
                    
                except Exception as e:
                    print(f"⚠️  Erro ao carregar {file_path}: {e}")
                    continue
        
        print(f"✅ Total de datasets personalizados: {len(all_conversations)} conversas")
        return all_conversations
    
    def balance_datasets(self, redis_data: List[Dict], custom_data: List[Dict], 
                        balance_ratio: float = 0.5) -> Dict[str, List[Dict]]:
        """
        Balancear dados do Redis com datasets personalizados
        
        Args:
            redis_data: Dados do cache Redis
            custom_data: Dados dos datasets personalizados  
            balance_ratio: Proporção de dados Redis (0.0 = só custom, 1.0 = só redis)
            
        Returns:
            Dados balanceados por categoria
        """
        print(f"⚖️  Balanceando datasets (Redis: {balance_ratio:.1%}, Custom: {1-balance_ratio:.1%})")
        
        # Calcular quantidades alvo
        total_redis = len(redis_data)
        total_custom = len(custom_data)
        
        if total_redis == 0 and total_custom == 0:
            print("❌ Nenhum dado disponível para balanceamento")
            return {}
        
        # Categorizar dados
        categorized = {
            "redis_real_usage": redis_data,
            "custom_datasets": custom_data,
            "balanced_mixed": []
        }
        
        # Criar mix balanceado
        if total_redis > 0 and total_custom > 0:
            # Calcular quantidades baseadas na proporção
            redis_count = int(min(total_redis, total_custom * balance_ratio / (1 - balance_ratio)))
            custom_count = int(min(total_custom, total_redis * (1 - balance_ratio) / balance_ratio))
            
            # Selecionar amostras balanceadas
            balanced_data = redis_data[:redis_count] + custom_data[:custom_count]
            categorized["balanced_mixed"] = balanced_data
            
            print(f"📊 Mix balanceado: {redis_count} Redis + {custom_count} Custom = {len(balanced_data)} total")
        
        return categorized
    
    def categorize_by_domain(self, conversations: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorizar conversas por domínio usando múltiplos critérios"""
        print("🏷️  Categorizando por domínio...")
        
        categories = {
            "business": [],
            "technical": [], 
            "support": [],
            "general": [],
            "custom": []
        }
        
        # Keywords expandidas para classificação
        keywords = {
            "business": [
                "roi", "lucro", "receita", "investimento", "negócio", "empresa", 
                "marketing", "vendas", "cliente", "mercado", "estratégia", "plano"
            ],
            "technical": [
                "api", "código", "programação", "docker", "redis", "ollama", "erro", 
                "debug", "sistema", "servidor", "banco", "dados", "cache", "python"
            ],
            "support": [
                "ajuda", "problema", "senha", "login", "acesso", "suporte", "como fazer",
                "não consigo", "erro", "falha", "dúvida", "orientação"
            ]
        }
        
        for conv in conversations:
            input_lower = conv.get("input", "").lower()
            output_lower = conv.get("output", "").lower()
            
            # Verificar se já tem domínio definido (de dataset personalizado)
            if "domain" in conv and conv["domain"] not in ["unknown", "imported", "general"]:
                domain = conv["domain"]
                if domain in categories:
                    categories[domain].append(conv)
                else:
                    categories["custom"].append(conv)
                continue
            
            # Classificar por keywords
            categorized = False
            for category, kws in keywords.items():
                if any(kw in input_lower or kw in output_lower for kw in kws):
                    categories[category].append(conv)
                    categorized = True
                    break
            
            # Se não foi categorizado, vai para geral
            if not categorized:
                categories["general"].append(conv)
        
        # Mostrar estatísticas
        for category, convs in categories.items():
            if convs:
                print(f"  • {category.capitalize()}: {len(convs)} conversas")
        
        return categories
    
    async def create_hybrid_training_data(
        self, 
        days_back: int = 7,
        balance_ratio: float = 0.5,
        include_datasets: List[str] = ["*.json"]
    ) -> Dict[str, Any]:
        """
        Criar dados de treinamento híbridos
        
        Args:
            days_back: Dias de histórico do Redis
            balance_ratio: Proporção Redis/Custom (0.5 = 50/50)
            include_datasets: Patterns de arquivos de dataset
            
        Returns:
            Estrutura completa de dados de treinamento
        """
        print("🧠 Criando dados de treinamento híbridos...")
        print("=" * 50)
        
        # 1. Coletar dados do Redis
        redis_data = await self.collect_redis_data(days_back)
        
        # 2. Carregar datasets personalizados
        custom_data = self.load_custom_datasets(include_datasets)
        
        # 3. Balancear os dados
        balanced_data = self.balance_datasets(redis_data, custom_data, balance_ratio)
        
        # 4. Categorizar por domínio
        all_conversations = []
        for category_data in balanced_data.values():
            all_conversations.extend(category_data)
        
        categorized = self.categorize_by_domain(all_conversations)
        
        # 5. Criar estrutura final
        training_structure = {
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "redis_conversations": len(redis_data),
                "custom_conversations": len(custom_data),
                "total_conversations": len(all_conversations),
                "balance_ratio": balance_ratio,
                "days_back": days_back
            },
            "raw_data": {
                "redis": redis_data,
                "custom": custom_data
            },
            "balanced_data": balanced_data,
            "categorized_data": categorized,
            "domains": {domain: len(convs) for domain, convs in categorized.items() if convs}
        }
        
        # 6. Salvar dados completos
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.training_data_dir / f"hybrid_training_data_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(training_structure, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Dados híbridos salvos: {output_file.name}")
        print(f"📊 Resumo final:")
        print(f"   • Redis: {len(redis_data)} conversas")
        print(f"   • Custom: {len(custom_data)} conversas") 
        print(f"   • Total: {len(all_conversations)} conversas")
        print(f"   • Domínios: {len([d for d, c in categorized.items() if c])}")
        
        return training_structure

async def main():
    """Demonstração do sistema híbrido"""
    print("🔄 Sistema Híbrido de Fine-Tuning")
    print("=" * 50)
    
    # Primeiro, criar alguns datasets de exemplo se não existirem
    training_dir = Path("training_data")
    if not any(training_dir.glob("*.json")):
        print("📝 Criando datasets de exemplo...")
        from dataset_generator import create_sample_datasets
        create_sample_datasets()
    
    # Criar fine-tuner híbrido
    hybrid_tuner = HybridFineTuner()
    
    # Criar dados de treinamento híbridos
    training_data = await hybrid_tuner.create_hybrid_training_data(
        days_back=30,          # 30 dias de cache Redis
        balance_ratio=0.7,     # 70% Redis, 30% datasets personalizados
        include_datasets=["*.json"]  # Incluir todos os JSONs
    )
    
    print(f"\n🎯 Próximos passos:")
    print(f"1. Revisar dados em: training_data/")
    print(f"2. Ajustar balance_ratio se necessário")
    print(f"3. Executar fine-tuning: python scripts/auto_fine_tune.py")
    print(f"4. Testar modelos especializados")

if __name__ == "__main__":
    asyncio.run(main())
