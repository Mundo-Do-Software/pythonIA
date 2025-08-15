#!/usr/bin/env python3
"""
Script de Exemplo - Criação de Dataset Personalizado
Mostra como criar datasets para diferentes domínios
"""

import sys
import os
from pathlib import Path

# Adicionar diretório raiz ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.fine_tuning.dataset_generator import DatasetGenerator

def create_my_business_dataset():
    """Exemplo: Dataset para meu negócio específico"""
    generator = DatasetGenerator()
    
    # Exemplo para uma empresa de tecnologia
    tech_business_conversations = [
        {
            "input": "Quais são os custos de desenvolvimento de um app?",
            "output": "Os custos de desenvolvimento de app variam de R$ 10.000 a R$ 500.000, dependendo da complexidade. Apps simples custam R$ 10-50k, médios R$ 50-150k, e complexos R$ 150k+. Fatores incluem plataformas (iOS/Android), funcionalidades, design e manutenção."
        },
        {
            "input": "Como precificar serviços de consultoria em TI?",
            "output": "Para precificar consultoria em TI: 1) Calcule seus custos (salário, impostos, infraestrutura), 2) Defina margem de lucro (30-50%), 3) Pesquise mercado (R$ 100-300/hora), 4) Considere valor entregue, 5) Ofereça pacotes mensais para recorrência."
        },
        {
            "input": "Qual o melhor modelo de negócio para SaaS?",
            "output": "Para SaaS, modelos eficazes incluem: 1) Freemium (gratuito + premium), 2) Assinatura mensal/anual, 3) Por usuário/funcionalidade, 4) Híbrido. Foque em LTV > CAC, churn baixo (<5% mensal), e crescimento recorrente. Teste diferentes preços com A/B testing."
        }
    ]
    
    return generator.create_conversation_dataset(
        tech_business_conversations, 
        "meu_negocio_tech", 
        "json"
    )

def create_my_support_dataset():
    """Exemplo: Dataset de suporte ao cliente personalizado"""
    generator = DatasetGenerator()
    
    # Exemplo para suporte de software
    support_conversations = [
        {
            "input": "O sistema está lento, o que fazer?",
            "output": "Para resolver lentidão: 1) Verifique conexão internet, 2) Feche abas/programas desnecessários, 3) Limpe cache do navegador, 4) Reinicie o sistema, 5) Se persistir, entre em contato informando: SO, navegador, e passos reproduzir o problema."
        },
        {
            "input": "Como fazer backup dos meus dados?",
            "output": "Para backup seguro: 1) Acesse Configurações > Backup, 2) Selecione dados para salvar, 3) Escolha local (nuvem/local), 4) Configure frequência automática, 5) Teste restauração mensalmente. Recomendamos backup diário automático para nuvem."
        },
        {
            "input": "Posso integrar com outras ferramentas?",
            "output": "Sim! Oferecemos integrações com: Slack, Teams, Zapier, Google Workspace, Office 365. Acesse Integrações no menu, escolha a ferramenta, siga o wizard de configuração. Para integrações personalizadas, consulte nossa API em docs.empresa.com/api."
        }
    ]
    
    return generator.create_conversation_dataset(
        support_conversations,
        "meu_suporte_personalizado",
        "json"
    )

def create_domain_specific_dataset():
    """Exemplo: Dataset específico do seu domínio"""
    generator = DatasetGenerator()
    
    # Exemplos para área específica (ex: saúde, educação, e-commerce)
    domain_examples = [
        "telemedicina",
        "prescrição digital", 
        "agendamento online",
        "prontuário eletrônico",
        "consulta virtual"
    ]
    
    # O sistema vai gerar automaticamente variações usando templates
    return generator.create_domain_specific_dataset("saude_digital", domain_examples)

def create_qa_dataset():
    """Exemplo: Dataset de perguntas e respostas"""
    generator = DatasetGenerator()
    
    qa_pairs = [
        {
            "question": "Como funciona a IA no nosso sistema?",
            "answer": "Nossa IA usa modelos de linguagem avançados para entender contexto e gerar respostas precisas. Combinamos cache semântico para velocidade com fine-tuning contínuo para melhorar a qualidade das respostas baseada no uso real.",
            "context": "Sistema de IA empresarial"
        },
        {
            "question": "Quais são os benefícios do cache semântico?",
            "answer": "O cache semântico oferece: 1) Velocidade 800x+ maior, 2) Redução de custos computacionais, 3) Respostas consistentes para perguntas similares, 4) Melhoria contínua da experiência do usuário.",
            "context": "Performance e otimização"
        }
    ]
    
    return generator.create_qa_dataset(qa_pairs, "perguntas_frequentes", include_context=True)

def import_from_my_csv():
    """Exemplo: Importar de arquivo CSV"""
    generator = DatasetGenerator()
    
    # Primeiro, crie um CSV de exemplo
    import csv
    csv_file = "training_data/exemplo_dataset.csv"
    
    # Criar CSV de exemplo se não existir
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['input', 'output', 'categoria'])
            writer.writerow(['Como configurar SSL?', 'Para SSL: 1) Obtenha certificado, 2) Configure servidor, 3) Teste conexão HTTPS', 'seguranca'])
            writer.writerow(['Backup automático funciona?', 'Sim, backup automático roda diariamente às 2h. Verifique logs em /var/log/backup.log', 'backup'])
        
        print(f"📝 CSV de exemplo criado: {csv_file}")
        
        # Importar o CSV
        return generator.import_from_csv(csv_file, "importado_csv")
        
    except Exception as e:
        print(f"⚠️  Erro ao criar/importar CSV: {e}")
        return None

def combine_all_datasets():
    """Exemplo: Combinar múltiplos datasets"""
    generator = DatasetGenerator()
    
    # Criar vários datasets
    datasets = []
    
    business_file = create_my_business_dataset()
    if business_file:
        datasets.append(business_file)
    
    support_file = create_my_support_dataset()
    if support_file:
        datasets.append(support_file)
    
    qa_file = create_qa_dataset()
    if qa_file:
        datasets.append(qa_file)
    
    csv_file = import_from_my_csv()
    if csv_file:
        datasets.append(csv_file)
    
    # Combinar todos
    if datasets:
        combined_file = generator.merge_datasets(datasets, "meu_dataset_completo")
        return combined_file
    
    return None

def main():
    """Criar datasets personalizados de exemplo"""
    print("🎨 Criação de Datasets Personalizados")
    print("=" * 50)
    
    print("\n1. 🏢 Criando dataset de negócios...")
    business_file = create_my_business_dataset()
    
    print("\n2. 🎧 Criando dataset de suporte...")
    support_file = create_my_support_dataset()
    
    print("\n3. 🏥 Criando dataset específico (saúde)...")
    domain_file = create_domain_specific_dataset()
    
    print("\n4. ❓ Criando dataset de Q&A...")
    qa_file = create_qa_dataset()
    
    print("\n5. 📊 Importando de CSV...")
    csv_file = import_from_my_csv()
    
    print("\n6. 🔄 Combinando todos os datasets...")
    combined_file = combine_all_datasets()
    
    print(f"\n🎉 Datasets criados com sucesso!")
    print(f"📁 Verifique a pasta: training_data/")
    print(f"\n🚀 Próximos passos:")
    print(f"1. Edite os exemplos acima com seus dados reais")
    print(f"2. Execute: python scripts/create_my_datasets.py")
    print(f"3. Execute fine-tuning: python scripts/hybrid_fine_tuning.py")
    print(f"4. Teste o sistema treinado!")
    
    print(f"\n💡 Dicas:")
    print(f"• Adicione 20-50 exemplos por domínio para melhor qualidade")
    print(f"• Use linguagem natural nas perguntas")
    print(f"• Respostas devem ser detalhadas e úteis")
    print(f"• Teste diferentes formatos: JSON, CSV, YAML")

if __name__ == "__main__":
    main()
