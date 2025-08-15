#!/usr/bin/env python3
"""
Script para criar dataset personalizado de e-commerce
Exemplo prático para demonstração
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.fine_tuning.dataset_generator import DatasetGenerator

def create_ecommerce_dataset():
    """Criar dataset específico para suporte de e-commerce"""
    generator = DatasetGenerator()
    
    print("🛒 Criando Dataset de E-commerce")
    print("=" * 50)
    
    # Dataset específico para e-commerce
    ecommerce_conversations = [
        {
            "input": "Como faço para cancelar meu pedido?",
            "output": "Para cancelar seu pedido: 1) Acesse 'Meus Pedidos' no site, 2) Clique em 'Cancelar' ao lado do pedido desejado, 3) Confirme o cancelamento. Se o pedido já foi enviado, você pode recusá-lo na entrega. Estornos são processados em até 5 dias úteis."
        },
        {
            "input": "Qual o prazo de entrega para São Paulo?",
            "output": "Para São Paulo capital: Entrega expressa (24h) ou padrão (2-3 dias úteis). Para Grande São Paulo: 2-4 dias úteis. Para interior: 3-7 dias úteis. Você pode acompanhar o rastreamento pelo código enviado por email."
        },
        {
            "input": "Como trocar um produto defeituoso?",
            "output": "Para trocar produto defeituoso: 1) Acesse 'Trocas e Devoluções', 2) Informe o motivo (defeito), 3) Agende a coleta gratuita, 4) Novo produto será enviado após análise. Processo leva 7-10 dias úteis. Envie fotos do defeito para agilizar."
        },
        {
            "input": "Posso parcelar sem juros?",
            "output": "Sim! Oferecemos parcelamento sem juros em até 12x no cartão de crédito para compras acima de R$ 200. Para valores menores, até 6x sem juros. No PIX, desconto de 5%. Boleto à vista tem 2% de desconto."
        },
        {
            "input": "O produto não chegou no prazo",
            "output": "Lamento pelo atraso. Vamos verificar: 1) Confirme seu endereço de entrega, 2) Verifique com portaria/vizinhos, 3) Se confirmado o atraso, ressarcimos o frete ou oferecemos desconto na próxima compra. Prazo máximo é de 15 dias para acionar transportadora."
        },
        {
            "input": "Como alterar o endereço de entrega?",
            "output": "Para alterar endereço: 1) Se pedido ainda não foi faturado, acesse 'Meus Pedidos' e clique em 'Alterar endereço', 2) Se já foi enviado, entre em contato conosco para tentar interceptar junto à transportadora, 3) Como alternativa, você pode recusar a entrega e repediremos."
        },
        {
            "input": "Qual a política de devolução?",
            "output": "Nossa política de devolução: 1) Até 7 dias corridos após recebimento (Código de Defesa do Consumidor), 2) Produto deve estar em perfeito estado, 3) Coleta gratuita em todo Brasil, 4) Estorno em até 10 dias úteis. Para produtos personalizados, não aceitamos devolução."
        },
        {
            "input": "Como acompanhar meu pedido?",
            "output": "Para acompanhar seu pedido: 1) Use o código de rastreamento enviado por email, 2) Acesse 'Meus Pedidos' em sua conta, 3) Consulte diretamente no site dos Correios/transportadora, 4) Receba notificações automáticas por WhatsApp cadastrando seu número."
        },
        {
            "input": "Vocês têm loja física?",
            "output": "Somos 100% online, o que nos permite oferecer melhores preços. Mas oferecemos: 1) Retirada em pontos parceiros em SP, RJ e BH, 2) Showroom para produtos de alto valor (agende visita), 3) Suporte via chat, email e telefone, 4) Garantia estendida em produtos eletrônicos."
        },
        {
            "input": "O produto está em promoção?",
            "output": "Verifico para você! Nossas promoções incluem: 1) Liquidações semanais às quartas, 2) Black Friday e Cyber Monday com até 70% off, 3) Cupons exclusivos por email, 4) Cashback para clientes Premium, 5) Desconto progressivo por quantidade. Cadastre-se na newsletter para ofertas exclusivas!"
        }
    ]
    
    # Criar o dataset
    dataset_name = "ecommerce_suporte"
    file_path = generator.create_conversation_dataset(ecommerce_conversations, dataset_name)
    
    print(f"✅ Dataset criado: {file_path}")
    print(f"📊 Total de exemplos: {len(ecommerce_conversations)}")
    
    return file_path

def create_technical_dataset():
    """Criar dataset para suporte técnico de software"""
    generator = DatasetGenerator()
    
    print("\n🔧 Criando Dataset Técnico")
    print("=" * 50)
    
    technical_conversations = [
        {
            "input": "A API está retornando erro 500",
            "output": "Para resolver erro 500: 1) Verifique os logs do servidor em /var/log/, 2) Confirme se o banco de dados está conectado, 3) Teste a conexão Redis com 'redis-cli ping', 4) Reinicie os serviços com 'docker-compose restart', 5) Se persistir, verifique memória RAM disponível."
        },
        {
            "input": "Como configurar SSL no Docker?",
            "output": "Para SSL no Docker: 1) Obtenha certificados (Let's Encrypt gratuito), 2) Monte volumes dos certificados no container, 3) Configure nginx/apache para SSL, 4) Redirecione HTTP para HTTPS, 5) Teste com 'curl -I https://seudominio.com'. Exemplo: 'docker run -v /etc/ssl:/ssl nginx'."
        },
        {
            "input": "O Redis não está conectando",
            "output": "Para debug Redis: 1) Verifique se está rodando 'docker ps | grep redis', 2) Teste conexão 'redis-cli -h localhost -p 6379 ping', 3) Confirme firewall/porta liberada, 4) Verifique logs 'docker logs redis-container', 5) Reinicie se necessário 'docker restart redis'."
        },
        {
            "input": "Como otimizar performance da API?",
            "output": "Para otimizar API: 1) Implemente cache Redis/Memcached, 2) Use connection pooling no banco, 3) Otimize queries SQL (índices), 4) Configure load balancer, 5) Use CDN para assets, 6) Monitore com APM (New Relic/DataDog), 7) Considere cache semântico para LLMs."
        },
        {
            "input": "Backup automático não funciona",
            "output": "Para backup automático: 1) Verifique cron job 'crontab -l', 2) Confirme permissões de escrita no destino, 3) Teste script manualmente, 4) Verifique espaço em disco 'df -h', 5) Configure logs do backup, 6) Use ferramentas como rsync ou duplicati. Exemplo: '0 2 * * * /scripts/backup.sh'."
        }
    ]
    
    dataset_name = "suporte_tecnico"
    file_path = generator.create_conversation_dataset(technical_conversations, dataset_name)
    
    print(f"✅ Dataset criado: {file_path}")
    print(f"📊 Total de exemplos: {len(technical_conversations)}")
    
    return file_path

if __name__ == "__main__":
    print("🎯 Criação de Datasets Personalizados")
    print("=" * 60)
    
    # Criar datasets
    ecommerce_file = create_ecommerce_dataset()
    technical_file = create_technical_dataset()
    
    print(f"\n🎉 Datasets criados com sucesso!")
    print(f"📁 Arquivos salvos em: training_data/")
    print(f"\n🚀 Próximo passo:")
    print(f"   python src/fine_tuning/real_fine_tuning.py")
