#!/usr/bin/env python3
"""
Script para testar o modelo fine-tuned via API
Simula testes do Postman com diferentes cenários
"""

import requests
import json
import time
from datetime import datetime

class APITester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def test_health(self):
        """Testar endpoint de saúde"""
        print("🏥 Testando Health Check...")
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API Status: {data.get('status')}")
                print(f"📊 Backend: {data.get('backend')}")
                print(f"🤖 Model: {data.get('model')}")
                return True
            else:
                print(f"❌ Health check falhou: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            return False
    
    def test_chat(self, message, expected_domain=None):
        """Testar endpoint de chat"""
        print(f"\n💬 Testando: '{message}'")
        print("-" * 60)
        
        payload = {
            "model": "mistral",
            "messages": [
                {"role": "user", "content": message}
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }
        
        try:
            start_time = time.time()
            response = self.session.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                response_time = end_time - start_time
                
                print(f"✅ Status: {response.status_code}")
                print(f"⏱️  Tempo: {response_time:.2f}s")
                
                # Extrair resposta do formato OpenAI
                choices = data.get('choices', [])
                if choices:
                    message_content = choices[0].get('message', {}).get('content', 'N/A')
                    print(f"🤖 Resposta: {message_content}")
                else:
                    print(f"🤖 Resposta: {data.get('response', 'N/A')}")
                
                # Verificar se veio do cache
                if 'cached' in data:
                    print(f"💾 Cache: {'HIT' if data['cached'] else 'MISS'}")
                
                # Verificar se foi usado fine-tuning (se implementado)
                if 'fine_tuned' in data:
                    print(f"🧠 Fine-tuned: {data['fine_tuned']}")
                    if expected_domain and 'domain' in data:
                        domain = data['domain']
                        if domain == expected_domain:
                            print(f"🎯 Domínio correto: {domain} ✅")
                        else:
                            print(f"⚠️  Domínio esperado: {expected_domain}, obtido: {domain}")
                
                return True
            else:
                print(f"❌ Erro: {response.status_code}")
                print(f"📄 Resposta: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return False
    
    def run_ecommerce_tests(self):
        """Executar testes específicos de e-commerce"""
        print(f"\n🛒 TESTES DE E-COMMERCE")
        print("=" * 60)
        
        ecommerce_questions = [
            ("Como faço para cancelar meu pedido?", "ecommerce_suporte"),
            ("Qual o prazo de entrega para São Paulo?", "ecommerce_suporte"),
            ("Como trocar um produto defeituoso?", "ecommerce_suporte"),
            ("Posso parcelar sem juros?", "ecommerce_suporte"),
            ("O produto não chegou no prazo", "ecommerce_suporte"),
        ]
        
        results = []
        for question, expected_domain in ecommerce_questions:
            success = self.test_chat(question, expected_domain)
            results.append(success)
            time.sleep(1)  # Evitar rate limiting
        
        return results
    
    def run_technical_tests(self):
        """Executar testes técnicos"""
        print(f"\n🔧 TESTES TÉCNICOS")
        print("=" * 60)
        
        technical_questions = [
            ("A API está retornando erro 500", "suporte_tecnico"),
            ("Como configurar SSL no Docker?", "suporte_tecnico"),
            ("O Redis não está conectando", "suporte_tecnico"),
            ("Como otimizar performance da API?", "suporte_tecnico"),
        ]
        
        results = []
        for question, expected_domain in technical_questions:
            success = self.test_chat(question, expected_domain)
            results.append(success)
            time.sleep(1)
        
        return results
    
    def run_general_tests(self):
        """Executar testes gerais"""
        print(f"\n🌐 TESTES GERAIS")
        print("=" * 60)
        
        general_questions = [
            "Olá, como você pode me ajudar?",
            "Qual é o seu nome?",
            "Que tipo de suporte você oferece?",
            "Como funciona o sistema?",
        ]
        
        results = []
        for question in general_questions:
            success = self.test_chat(question)
            results.append(success)
            time.sleep(1)
        
        return results
    
    def run_performance_test(self):
        """Teste de performance - múltiplas requisições"""
        print(f"\n⚡ TESTE DE PERFORMANCE")
        print("=" * 60)
        
        test_message = "Como cancelar pedido?"
        num_requests = 5
        
        times = []
        print(f"🚀 Enviando {num_requests} requisições...")
        
        for i in range(num_requests):
            start_time = time.time()
            response = self.session.post(
                f"{self.base_url}/chat/completions",
                json={"model": "mistral", "messages": [{"role": "user", "content": test_message}]},
                headers={"Content-Type": "application/json"}
            )
            end_time = time.time()
            
            if response.status_code == 200:
                response_time = end_time - start_time
                times.append(response_time)
                data = response.json()
                cached = data.get('cached', False)
                print(f"  {i+1}. {response_time:.3f}s {'(cached)' if cached else '(fresh)'}")
            else:
                print(f"  {i+1}. ERRO: {response.status_code}")
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            print(f"\n📊 Estatísticas:")
            print(f"   • Média: {avg_time:.3f}s")
            print(f"   • Mínimo: {min_time:.3f}s")
            print(f"   • Máximo: {max_time:.3f}s")
            print(f"   • Sucesso: {len(times)}/{num_requests}")

def main():
    """Executar todos os testes"""
    print("🧪 TESTE COMPLETO DO MODELO FINE-TUNED")
    print("=" * 70)
    print(f"⏰ Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = APITester()
    
    # 1. Teste de saúde
    if not tester.test_health():
        print("❌ API não está funcionando. Verifique se está rodando.")
        return
    
    # 2. Testes de E-commerce
    ecommerce_results = tester.run_ecommerce_tests()
    
    # 3. Testes técnicos
    technical_results = tester.run_technical_tests()
    
    # 4. Testes gerais
    general_results = tester.run_general_tests()
    
    # 5. Teste de performance
    tester.run_performance_test()
    
    # Resumo
    print(f"\n📊 RESUMO DOS TESTES")
    print("=" * 70)
    print(f"🛒 E-commerce: {sum(ecommerce_results)}/{len(ecommerce_results)} ✅")
    print(f"🔧 Técnico: {sum(technical_results)}/{len(technical_results)} ✅")
    print(f"🌐 Geral: {sum(general_results)}/{len(general_results)} ✅")
    
    total_success = sum(ecommerce_results) + sum(technical_results) + sum(general_results)
    total_tests = len(ecommerce_results) + len(technical_results) + len(general_results)
    
    print(f"\n🎯 RESULTADO FINAL: {total_success}/{total_tests} testes passaram")
    
    if total_success == total_tests:
        print("🎉 TODOS OS TESTES PASSARAM! Modelo fine-tuned funcionando perfeitamente!")
    elif total_success > total_tests * 0.8:
        print("✅ MAIORIA DOS TESTES PASSOU! Sistema funcionando bem.")
    else:
        print("⚠️  ALGUNS TESTES FALHARAM. Verifique a configuração.")

if __name__ == "__main__":
    main()
