import requests
import time
import json

OLLAMA_URL = 'http://ollama-server:11434'
available_models = []

try:
    print('DEBUG: Iniciando list_models()')
    response = requests.get(f'{OLLAMA_URL}/api/tags', timeout=5)
    print(f'DEBUG: Status da resposta: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()  
        print(f'DEBUG: Dados recebidos: {len(data.get("models", []))} modelos')
        
        ollama_models = data.get('models', [])
        
        for model in ollama_models:
            full_name = model['name']
            print(f'DEBUG: Processando modelo: {full_name}')
            
            if full_name == 'mistral:latest':
                model_id = 'mistral'
            elif full_name == 'llama3.2:3b':
                model_id = 'llama3.2'
            else:
                model_id = full_name.split(':')[0]
            
            model_entry = {
                'id': model_id,
                'object': 'model',
                'created': int(time.time()),
                'owned_by': 'local'
            }
            
            available_models.append(model_entry)
            print(f'DEBUG: Adicionado modelo: {model_id}')
            
except Exception as e:
    print(f'ERRO: {e}')
    import traceback
    traceback.print_exc()

print(f'DEBUG: Total de modelos processados: {len(available_models)}')
for m in available_models:
    print(f'  - {m["id"]}')

print('\nResultado final:')
result = {
    "object": "list",
    "data": available_models
}
print(json.dumps(result, indent=2))
