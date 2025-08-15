# =============================================================================
# FINE-TUNING MODULE - LoRA Implementation
# =============================================================================

import os
import json
import torch
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import logging

class LoRAFineTuner:
    """
    Fine-tuning usando LoRA (Low-Rank Adaptation)
    Permite treinar adaptadores específicos sem modificar o modelo base
    """
    
    def __init__(self, base_model: str = "mistral:7b"):
        self.base_model = base_model
        self.lora_dir = Path("loras")
        self.training_dir = Path("training_data")
        self.setup_directories()
        
    def setup_directories(self):
        """Criar diretórios necessários"""
        self.lora_dir.mkdir(exist_ok=True)
        self.training_dir.mkdir(exist_ok=True)
        (self.lora_dir / "domain_specific").mkdir(exist_ok=True)
        
    def prepare_dataset(self, conversations: List[Dict]) -> str:
        """
        Preparar dataset no formato correto para fine-tuning
        
        Args:
            conversations: Lista de conversas {"input": "...", "output": "..."}
            
        Returns:
            Caminho para o arquivo de dataset processado
        """
        dataset_path = self.training_dir / f"dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        
        with open(dataset_path, 'w', encoding='utf-8') as f:
            for conv in conversations:
                # Formato para Ollama fine-tuning
                entry = {
                    "messages": [
                        {"role": "user", "content": conv["input"]},
                        {"role": "assistant", "content": conv["output"]}
                    ]
                }
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
                
        return str(dataset_path)
    
    def train_lora_adapter(self, 
                          dataset_path: str,
                          adapter_name: str,
                          domain: str = "general",
                          epochs: int = 3,
                          learning_rate: float = 1e-4) -> str:
        """
        Treinar adaptador LoRA
        
        Args:
            dataset_path: Caminho para dataset de treinamento
            adapter_name: Nome do adaptador
            domain: Domínio específico (customer_support, technical, etc)
            epochs: Número de épocas de treinamento
            learning_rate: Taxa de aprendizagem
            
        Returns:
            Caminho para o adaptador treinado
        """
        adapter_path = self.lora_dir / "domain_specific" / f"{adapter_name}.safetensors"
        
        # Comando para treinar com Ollama (exemplo)
        training_config = {
            "base_model": self.base_model,
            "dataset": dataset_path,
            "output": str(adapter_path),
            "epochs": epochs,
            "learning_rate": learning_rate,
            "lora_rank": 16,
            "lora_alpha": 32,
            "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj"]
        }
        
        logging.info(f"Iniciando treinamento LoRA: {adapter_name}")
        logging.info(f"Config: {training_config}")
        
        # Aqui implementaria a chamada real para o sistema de treinamento
        # Por exemplo: subprocess.run(["ollama", "fine-tune", "--config", config_file])
        
        return str(adapter_path)
    
    def load_adapter(self, adapter_path: str, model_name: str) -> str:
        """
        Carregar adaptador LoRA no Ollama
        
        Args:
            adapter_path: Caminho para o adaptador
            model_name: Nome para o modelo com adaptador
            
        Returns:
            Nome do modelo carregado
        """
        # Comando para carregar adaptador no Ollama
        # ollama create modelo_personalizado -f Modelfile_com_lora
        
        modelfile_content = f"""
FROM {self.base_model}
ADAPTER {adapter_path}
PARAMETER temperature 0.7
PARAMETER top_p 0.9
"""
        
        modelfile_path = self.lora_dir / f"{model_name}.Modelfile"
        with open(modelfile_path, 'w') as f:
            f.write(modelfile_content)
            
        return model_name
    
    def collect_training_data_from_cache(self, min_similarity: float = 0.9) -> List[Dict]:
        """
        Coletar dados de treinamento do cache Redis
        Usa interações reais dos usuários como dataset
        """
        # Conectar ao Redis e extrair conversas de alta qualidade
        # Filtrar por similaridade para pegar exemplos únicos
        pass
    
    def auto_fine_tune_from_usage(self, domain: str, min_examples: int = 100):
        """
        Fine-tuning automático baseado no uso real
        Coleta dados do cache e treina adaptador específico
        """
        # 1. Coletar dados do Redis cache
        training_data = self.collect_training_data_from_cache()
        
        if len(training_data) < min_examples:
            logging.warning(f"Poucos exemplos ({len(training_data)}) para domínio {domain}")
            return
            
        # 2. Preparar dataset
        dataset_path = self.prepare_dataset(training_data)
        
        # 3. Treinar adaptador
        adapter_name = f"{domain}_{datetime.now().strftime('%Y%m%d')}"
        adapter_path = self.train_lora_adapter(dataset_path, adapter_name, domain)
        
        # 4. Carregar no sistema
        model_name = f"{self.base_model}-{domain}"
        self.load_adapter(adapter_path, model_name)
        
        logging.info(f"Fine-tuning automático concluído: {model_name}")


class DomainSpecificTrainer:
    """Treinador para domínios específicos"""
    
    def __init__(self):
        self.fine_tuner = LoRAFineTuner()
        
    def train_customer_support(self, support_conversations: List[Dict]):
        """Treinar para atendimento ao cliente"""
        dataset_path = self.fine_tuner.prepare_dataset(support_conversations)
        return self.fine_tuner.train_lora_adapter(
            dataset_path, 
            "customer_support",
            domain="support",
            epochs=5
        )
    
    def train_technical_docs(self, tech_qa_pairs: List[Dict]):
        """Treinar para documentação técnica"""
        dataset_path = self.fine_tuner.prepare_dataset(tech_qa_pairs)
        return self.fine_tuner.train_lora_adapter(
            dataset_path,
            "technical_docs", 
            domain="technical",
            epochs=3
        )
    
    def train_portuguese_legal(self, legal_documents: List[Dict]):
        """Treinar para documentos jurídicos em português"""
        dataset_path = self.fine_tuner.prepare_dataset(legal_documents)
        return self.fine_tuner.train_lora_adapter(
            dataset_path,
            "portuguese_legal",
            domain="legal", 
            epochs=4,
            learning_rate=5e-5  # Menor LR para domínio específico
        )


# Exemplo de uso
if __name__ == "__main__":
    # Dados de exemplo para customer support
    support_data = [
        {
            "input": "Como faço login no sistema?",
            "output": "Para fazer login, acesse a página inicial e clique em 'Entrar'. Digite seu email e senha cadastrados. Se esqueceu a senha, clique em 'Esqueci minha senha' para redefinir."
        },
        {
            "input": "Não consigo acessar minha conta",
            "output": "Vamos resolver isso! Primeiro, verifique se está usando o email correto. Tente redefinir sua senha. Se o problema persistir, entre em contato conosco com seu email cadastrado."
        }
        # ... mais exemplos
    ]
    
    # Treinar adaptador
    trainer = DomainSpecificTrainer()
    adapter_path = trainer.train_customer_support(support_data)
    print(f"Adaptador treinado: {adapter_path}")
