#!/usr/bin/env python3
"""
Teste simplificado do sistema de fine-tuning
Coleta dados do cache Redis sem dependências pesadas
"""

import asyncio
import json
import redis.asyncio as redis
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging
from pathlib import Path

class SimplifiedFineTuningTest:
    """
    Teste simplificado para verificar coleta de dados do cache
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        
    async def test_redis_connection(self):
        """Testar conexão com Redis"""
        try:
            redis_client = redis.from_url(self.redis_url, decode_responses=True)
            await redis_client.ping()
            print("✅ Conexão com Redis: OK")
            await redis_client.close()
            return True
        except Exception as e:
            print(f"❌ Erro na conexão Redis: {e}")
            return False
    
    async def collect_cache_data(self, days_back: int = 7) -> List[Dict]:
        """
        Coletar dados de conversas do cache Redis
        """
        redis_client = redis.from_url(self.redis_url, decode_responses=True)
        training_data = []
        
        try:
            # Buscar todas as chaves de cache
            cache_keys = await redis_client.keys("cache:*")
            print(f"🔍 Encontradas {len(cache_keys)} chaves de cache")
            
            if len(cache_keys) == 0:
                print("⚠️  Nenhuma entrada de cache encontrada")
                return training_data
            
            cutoff_date = datetime.now() - timedelta(days=days_back)
            valid_entries = 0
            
            for i, key in enumerate(cache_keys[:10]):  # Limitar a 10 para teste
                try:
                    cache_data = await redis_client.get(key)
                    if cache_data:
                        data = json.loads(cache_data)
                        
                        # Extrair pergunta original do cache key
                        query = key.replace("cache:", "").replace("_", " ")
                        
                        # Extrair resposta
                        response = ""
                        if 'response' in data:
                            choices = data['response'].get('choices', [])
                            if choices and len(choices) > 0:
                                message = choices[0].get('message', {})
                                response = message.get('content', '')
                        
                        if query and response:
                            training_entry = {
                                "input": query,
                                "output": response,
                                "timestamp": data.get('timestamp', datetime.now().isoformat()),
                                "similarity_used": data.get('similarity', 0)
                            }
                            training_data.append(training_entry)
                            valid_entries += 1
                            
                            print(f"  {i+1}. Query: {query[:50]}...")
                            print(f"      Response: {response[:50]}...")
                            
                except json.JSONDecodeError as e:
                    print(f"  ⚠️  Erro ao decodificar chave {key}: {e}")
                    continue
                except Exception as e:
                    print(f"  ⚠️  Erro ao processar chave {key}: {e}")
                    continue
                    
            print(f"✅ Coletadas {valid_entries} conversas válidas")
                    
        except Exception as e:
            print(f"❌ Erro ao coletar dados do cache: {e}")
        finally:
            await redis_client.close()
            
        return training_data
    
    def categorize_conversations(self, conversations: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Categorizar conversas por domínio usando keywords simples
        """
        categories = {
            "technical": [],
            "support": [],
            "legal": [],
            "general": []
        }
        
        # Keywords para classificação
        keywords = {
            "technical": ["api", "código", "programação", "docker", "redis", "ollama", "erro", "debug", "sistema"],
            "support": ["login", "senha", "acesso", "conta", "problema", "ajuda", "como fazer", "não consigo"],
            "legal": ["contrato", "lei", "jurídico", "legal", "direito", "processo", "advogado", "tribunal"]
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
    
    def save_training_data(self, conversations: List[Dict], filename: str = None):
        """Salvar dados de treinamento em arquivo"""
        if not filename:
            filename = f"training_data_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Criar diretório se não existir
        training_dir = Path("training_data")
        training_dir.mkdir(exist_ok=True)
        
        filepath = training_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "conversations": conversations,
                "total_count": len(conversations),
                "collected_at": datetime.now().isoformat(),
                "categorization": self.categorize_conversations(conversations)
            }, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Dados salvos em: {filepath}")
        return str(filepath)

async def main():
    """Teste principal do sistema de fine-tuning"""
    
    print("🧠 Teste do Sistema de Fine-Tuning")
    print("=" * 50)
    
    # Inicializar tester
    tester = SimplifiedFineTuningTest()
    
    # 1. Testar conexão Redis
    if not await tester.test_redis_connection():
        print("❌ Falha na conexão com Redis. Verifique se está rodando.")
        return
    
    # 2. Coletar dados do cache
    print("\n📊 Coletando dados do cache...")
    conversations = await tester.collect_cache_data(days_back=30)
    
    if not conversations:
        print("⚠️  Nenhuma conversa encontrada para fine-tuning")
        print("💡 Execute algumas consultas na API primeiro:")
        print("   curl -X POST http://localhost:5000/v1/chat/completions \\")
        print("        -H 'Content-Type: application/json' \\")
        print("        -d '{\"model\": \"auto\", \"messages\": [{\"role\": \"user\", \"content\": \"Olá\"}]}'")
        return
    
    # 3. Categorizar conversas
    print(f"\n🏷️  Categorizando {len(conversations)} conversas...")
    categorized = tester.categorize_conversations(conversations)
    
    print("📋 Resultados da categorização:")
    for category, convs in categorized.items():
        print(f"  • {category.capitalize()}: {len(convs)} conversas")
    
    # 4. Salvar dados para análise
    filepath = tester.save_training_data(conversations)
    
    # 5. Relatório final
    print(f"\n🎯 Resumo do Teste:")
    print(f"  • Conversas coletadas: {len(conversations)}")
    print(f"  • Dados salvos em: {filepath}")
    print(f"  • Status: ✅ Sistema funcionando")
    
    if len(conversations) >= 10:
        print("✅ Dados suficientes para fine-tuning real!")
    else:
        print("💡 Execute mais consultas para obter dados de treinamento")

if __name__ == "__main__":
    asyncio.run(main())
