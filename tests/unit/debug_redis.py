#!/usr/bin/env python3
"""
Teste simples para verificar dados no Redis
"""

import redis
import json

def main():
    """Teste simples do Redis"""
    print("🔍 Verificando dados no Redis...")
    
    # Conectar ao Redis
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    try:
        # Ping test
        r.ping()
        print("✅ Redis conectado")
        
        # Ver todas as chaves
        all_keys = list(r.keys("*"))
        print(f"📊 Total de chaves: {len(all_keys)}")
        
        if all_keys:
            print("\n🗝️  Chaves encontradas:")
            for i, key in enumerate(all_keys[:10]):  # Mostrar até 10
                value = r.get(key)
                print(f"  {i+1}. {key} = {str(value)[:100]}...")
                
                # Se parece com JSON, tentar decodificar
                if value and (value.startswith('{') or value.startswith('[')):
                    try:
                        data = json.loads(value)
                        print(f"      JSON válido com {len(data)} campos")
                        if isinstance(data, dict) and 'response' in data:
                            response = data.get('response', {})
                            if isinstance(response, dict) and 'choices' in response:
                                choices = response.get('choices', [])
                                if choices:
                                    content = choices[0].get('message', {}).get('content', '')
                                    print(f"      Resposta: {content[:50]}...")
                    except:
                        print("      Não é JSON válido")
        else:
            print("⚠️  Nenhuma chave encontrada")
            
        # Verificar TTL de algumas chaves
        if all_keys:
            print(f"\n⏰ TTL das primeiras chaves:")
            for key in all_keys[:3]:
                ttl = r.ttl(key)
                if ttl > 0:
                    print(f"  {key}: {ttl}s restantes")
                elif ttl == -1:
                    print(f"  {key}: sem expiração")
                else:
                    print(f"  {key}: já expirou")
                    
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
