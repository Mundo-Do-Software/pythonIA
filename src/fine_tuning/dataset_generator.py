#!/usr/bin/env python3
"""
Gerador de Datasets Personalizados para Fine-Tuning
Permite criar datasets customizados em diferentes formatos
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import yaml

class DatasetGenerator:
    """
    Gerador de datasets para fine-tuning personalizado
    Suporta múltiplos formatos: JSON, CSV, JSONL, YAML
    """
    
    def __init__(self, output_dir: str = "training_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def create_conversation_dataset(
        self, 
        conversations: List[Dict[str, str]], 
        domain: str = "custom",
        format: str = "json"
    ) -> str:
        """
        Criar dataset de conversas
        
        Args:
            conversations: Lista de conversas [{"input": "pergunta", "output": "resposta"}]
            domain: Domínio do dataset (ex: "business", "technical", "support")
            format: Formato do arquivo ("json", "csv", "jsonl", "yaml")
            
        Returns:
            Caminho do arquivo gerado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{domain}_dataset_{timestamp}.{format}"
        filepath = self.output_dir / filename
        
        # Adicionar metadados
        dataset = {
            "metadata": {
                "domain": domain,
                "created_at": datetime.now().isoformat(),
                "total_examples": len(conversations),
                "format_version": "1.0"
            },
            "conversations": conversations
        }
        
        # Salvar no formato solicitado
        if format == "json":
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(dataset, f, indent=2, ensure_ascii=False)
                
        elif format == "jsonl":
            with open(filepath, 'w', encoding='utf-8') as f:
                for conv in conversations:
                    json.dump(conv, f, ensure_ascii=False)
                    f.write('\n')
                    
        elif format == "csv":
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['input', 'output', 'domain'])
                writer.writeheader()
                for conv in conversations:
                    writer.writerow({**conv, 'domain': domain})
                    
        elif format == "yaml":
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(dataset, f, default_flow_style=False, allow_unicode=True)
                
        print(f"✅ Dataset '{domain}' criado: {filepath}")
        print(f"📊 Total de exemplos: {len(conversations)}")
        
        return str(filepath)
    
    def create_qa_dataset(
        self, 
        qa_pairs: List[Dict[str, str]], 
        domain: str = "qa",
        include_context: bool = False
    ) -> str:
        """
        Criar dataset de perguntas e respostas
        
        Args:
            qa_pairs: Lista de pares Q&A [{"question": "...", "answer": "..."}]
            domain: Domínio do dataset
            include_context: Se deve incluir contexto adicional
            
        Returns:
            Caminho do arquivo gerado
        """
        conversations = []
        
        for qa in qa_pairs:
            conv = {
                "input": qa.get("question", ""),
                "output": qa.get("answer", "")
            }
            
            if include_context and "context" in qa:
                conv["context"] = qa["context"]
                
            conversations.append(conv)
        
        return self.create_conversation_dataset(conversations, domain, "json")
    
    def create_domain_specific_dataset(self, domain: str, examples: List[str]) -> str:
        """
        Criar dataset específico de domínio com exemplos base
        
        Args:
            domain: Nome do domínio
            examples: Lista de exemplos/prompts base
            
        Returns:
            Caminho do arquivo gerado
        """
        conversations = []
        
        # Templates baseados no domínio
        templates = self._get_domain_templates(domain)
        
        for example in examples:
            for template in templates:
                conv = {
                    "input": template["input"].format(example=example),
                    "output": template["output"].format(example=example),
                    "domain": domain,
                    "template": template["name"]
                }
                conversations.append(conv)
        
        return self.create_conversation_dataset(conversations, domain, "json")
    
    def _get_domain_templates(self, domain: str) -> List[Dict]:
        """Templates por domínio"""
        templates = {
            "business": [
                {
                    "name": "analysis", 
                    "input": "Analyze this business scenario: {example}",
                    "output": "Business analysis for {example}: [Detailed analysis would go here]"
                },
                {
                    "name": "strategy",
                    "input": "What strategy would you recommend for {example}?",
                    "output": "Strategic recommendation for {example}: [Strategy details]"
                }
            ],
            "technical": [
                {
                    "name": "explanation",
                    "input": "Explain how {example} works",
                    "output": "Technical explanation of {example}: [Technical details]"
                },
                {
                    "name": "troubleshooting",
                    "input": "How to troubleshoot {example}?",
                    "output": "Troubleshooting steps for {example}: [Step by step guide]"
                }
            ],
            "support": [
                {
                    "name": "help",
                    "input": "I need help with {example}",
                    "output": "I can help you with {example}. [Helpful response]"
                },
                {
                    "name": "how_to",
                    "input": "How do I {example}?",
                    "output": "To {example}, follow these steps: [Instructions]"
                }
            ]
        }
        
        return templates.get(domain, [
            {
                "name": "general",
                "input": "Tell me about {example}",
                "output": "About {example}: [General information]"
            }
        ])
    
    def import_from_csv(self, csv_file: str, domain: str = "imported") -> str:
        """
        Importar dataset de arquivo CSV
        
        Args:
            csv_file: Caminho do arquivo CSV
            domain: Domínio para classificar o dataset
            
        Returns:
            Caminho do arquivo JSON gerado
        """
        conversations = []
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                conv = {
                    "input": row.get("input", row.get("question", "")),
                    "output": row.get("output", row.get("answer", "")),
                }
                
                # Adicionar campos extras se existirem
                for key, value in row.items():
                    if key not in ["input", "output", "question", "answer"] and value:
                        conv[key] = value
                        
                conversations.append(conv)
        
        print(f"📥 Importadas {len(conversations)} conversas de {csv_file}")
        return self.create_conversation_dataset(conversations, domain, "json")
    
    def merge_datasets(self, dataset_files: List[str], output_domain: str = "merged") -> str:
        """
        Combinar múltiplos datasets
        
        Args:
            dataset_files: Lista de arquivos de dataset para combinar
            output_domain: Nome do domínio combinado
            
        Returns:
            Caminho do arquivo combinado
        """
        all_conversations = []
        
        for file_path in dataset_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                conversations = data.get("conversations", [])
                if isinstance(data, list):  # Se o arquivo é uma lista direta
                    conversations = data
                    
                all_conversations.extend(conversations)
                print(f"📥 Carregadas {len(conversations)} conversas de {Path(file_path).name}")
                
            except Exception as e:
                print(f"⚠️  Erro ao carregar {file_path}: {e}")
                continue
        
        print(f"🔄 Total combinado: {len(all_conversations)} conversas")
        return self.create_conversation_dataset(all_conversations, output_domain, "json")

def create_sample_datasets():
    """Criar datasets de exemplo para demonstração"""
    generator = DatasetGenerator()
    
    # 1. Dataset de Negócios
    business_conversations = [
        {
            "input": "Como calcular o ROI de um investimento?",
            "output": "O ROI (Return on Investment) é calculado pela fórmula: ROI = (Ganho - Investimento) / Investimento × 100. Por exemplo, se você investiu R$ 1000 e ganhou R$ 1200, o ROI é 20%."
        },
        {
            "input": "Qual a diferença entre receita e lucro?",
            "output": "Receita é o total de dinheiro que entra na empresa através das vendas. Lucro é o que sobra após subtrair todos os custos da receita. Receita - Custos = Lucro."
        },
        {
            "input": "Como fazer um plano de negócios?",
            "output": "Um plano de negócios deve incluir: 1) Resumo executivo, 2) Análise de mercado, 3) Organização e gestão, 4) Produtos/serviços, 5) Marketing e vendas, 6) Projeções financeiras."
        }
    ]
    
    # 2. Dataset Técnico
    technical_conversations = [
        {
            "input": "O que é Docker?",
            "output": "Docker é uma plataforma de containerização que permite empacotar aplicações e suas dependências em containers leves e portáteis, garantindo consistência entre ambientes de desenvolvimento e produção."
        },
        {
            "input": "Como funciona o Redis?",
            "output": "Redis é um banco de dados em memória que funciona como cache ou armazenamento de estruturas de dados. Ele mantém dados na RAM para acesso ultra-rápido e oferece persistência opcional em disco."
        },
        {
            "input": "O que é API REST?",
            "output": "API REST é um estilo arquitetural para serviços web que usa métodos HTTP (GET, POST, PUT, DELETE) para operações CRUD, é stateless e utiliza URLs para identificar recursos."
        }
    ]
    
    # 3. Dataset de Suporte
    support_conversations = [
        {
            "input": "Esqueci minha senha, como recuperar?",
            "output": "Para recuperar sua senha: 1) Acesse a página de login, 2) Clique em 'Esqueci minha senha', 3) Digite seu email, 4) Verifique sua caixa de entrada e siga as instruções no email recebido."
        },
        {
            "input": "Como entrar em contato com suporte?",
            "output": "Você pode entrar em contato conosco através de: Email: suporte@empresa.com, Telefone: (11) 1234-5678, Chat online: disponível 24/7, ou Sistema de tickets: portal.empresa.com/suporte"
        },
        {
            "input": "Onde encontro a documentação?",
            "output": "Nossa documentação está disponível em: docs.empresa.com. Lá você encontra guias de início rápido, tutoriais detalhados, referência da API e exemplos práticos."
        }
    ]
    
    # Criar datasets
    business_file = generator.create_conversation_dataset(business_conversations, "business")
    technical_file = generator.create_conversation_dataset(technical_conversations, "technical")  
    support_file = generator.create_conversation_dataset(support_conversations, "support")
    
    # Criar dataset combinado
    combined_file = generator.merge_datasets([business_file, technical_file, support_file], "complete")
    
    print(f"\n🎉 Datasets de exemplo criados:")
    print(f"📊 Business: {Path(business_file).name}")
    print(f"🔧 Technical: {Path(technical_file).name}")
    print(f"🎧 Support: {Path(support_file).name}")
    print(f"🔄 Combined: {Path(combined_file).name}")
    
    return {
        "business": business_file,
        "technical": technical_file, 
        "support": support_file,
        "combined": combined_file
    }

def main():
    """Demonstração do gerador de datasets"""
    print("🧠 Gerador de Datasets Personalizados")
    print("=" * 50)
    
    # Criar datasets de exemplo
    datasets = create_sample_datasets()
    
    print(f"\n📁 Arquivos salvos em: training_data/")
    print(f"💡 Para usar seus próprios dados:")
    print(f"   1. Edite as listas de conversas no código")
    print(f"   2. Use generator.import_from_csv() para importar CSV")
    print(f"   3. Use generator.merge_datasets() para combinar")
    print(f"   4. Execute o fine-tuning: python scripts/auto_fine_tune.py")

if __name__ == "__main__":
    main()
