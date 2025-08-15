#!/usr/bin/env python3
"""
Versão simplificada da API com fine-tuning integrado
"""

import os
import time
import uuid
import json
import pickle
from typing import List, Dict, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Modelos de dados
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = "mistral"
    messages: List[ChatMessage]
    temperature: float = 0.7
    max_tokens: int = 512

# Classe simplificada do fine-tuned model
class SimpleFineTunedModel:
    def __init__(self):
        self.models = {}
        self.vectorizer = None
        self.loaded = False
        
    def load_model(self, model_path: str) -> bool:
        """Carregar modelo fine-tuned"""
        try:
            if Path(model_path).exists():
                with open(model_path, 'rb') as f:
                    data = pickle.load(f)
                    self.models = data.get('domain_models', {})
                    self.vectorizer = data.get('vectorizer')
                    self.loaded = True
                    print(f"✅ Fine-tuned model carregado: {len(self.models)} domínios")
                    return True
            return False
        except Exception as e:
            print(f"❌ Erro ao carregar modelo: {e}")
            return False
    
    def predict(self, query: str, top_k: int = 1) -> List[Dict]:
        """Fazer predição usando modelo fine-tuned"""
        if not self.loaded or not self.vectorizer:
            return []
            
        try:
            from sklearn.metrics.pairwise import cosine_similarity
            import numpy as np
            
            # Vetorizar query
            query_vector = self.vectorizer.transform([query])
            
            results = []
            
            # Testar cada domínio
            for domain, model_data in self.models.items():
                if 'examples' in model_data and 'responses' in model_data:
                    examples = model_data['examples']
                    responses = model_data['responses']
                    
                    # Calcular similaridade com cada exemplo
                    for i, (example, response) in enumerate(zip(examples, responses)):
                        example_vector = self.vectorizer.transform([example])
                        similarity = cosine_similarity(query_vector, example_vector)[0][0]
                        
                        results.append({
                            'domain': domain,
                            'response': response,
                            'confidence': similarity,
                            'example': example
                        })
            
            # Ordenar por confiança e retornar top_k
            results.sort(key=lambda x: x['confidence'], reverse=True)
            return results[:top_k]
            
        except Exception as e:
            print(f"❌ Erro na predição: {e}")
            return []

# Inicializar aplicação
app = FastAPI(title="Fine-Tuned LLM API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variável global para o modelo fine-tuned
fine_tuned_model = SimpleFineTunedModel()

@app.on_event("startup")
async def startup_event():
    """Carregar modelo fine-tuned na inicialização"""
    model_paths = [
        "models/fine_tuned_model_20250801_160218.pkl",
        "src/current_fine_tuned_model.pkl",
        "fine_tuned_model.pkl"
    ]
    
    for path in model_paths:
        if fine_tuned_model.load_model(path):
            print(f"🧠 Fine-tuned model carregado de: {path}")
            break
    else:
        print("⚠️  Nenhum modelo fine-tuned encontrado, usando respostas padrão")

@app.get("/")
async def health_check():
    """Health check"""
    return {
        "status": "running",
        "fine_tuned_loaded": fine_tuned_model.loaded,
        "domains": len(fine_tuned_model.models) if fine_tuned_model.loaded else 0,
        "api_version": "1.0.0"
    }

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """Endpoint principal usando fine-tuning"""
    
    try:
        start_time = time.time()
        
        # Extrair mensagem do usuário
        user_message = ""
        for msg in request.messages:
            if msg.role == "user":
                user_message = msg.content
                break
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Nenhuma mensagem do usuário encontrada")
        
        # Tentar usar modelo fine-tuned
        response_text = ""
        used_fine_tuned = False
        domain_used = "unknown"
        confidence = 0.0
        
        if fine_tuned_model.loaded:
            results = fine_tuned_model.predict(user_message, top_k=1)
            
            if results and len(results) > 0:
                best_result = results[0]
                confidence = best_result['confidence']
                
                # Usar fine-tuned se confiança for razoável
                if confidence > 0.3:  # 30% threshold
                    response_text = best_result['response']
                    domain_used = best_result['domain']
                    used_fine_tuned = True
                    print(f"🧠 Usando fine-tuned: {domain_used} ({confidence:.1%})")
        
        # Fallback para resposta padrão se fine-tuned não funcionar
        if not response_text:
            response_text = generate_fallback_response(user_message)
            used_fine_tuned = False
            domain_used = "fallback"
            print(f"💬 Usando resposta padrão")
        
        # Criar resposta no formato OpenAI
        response_time = time.time() - start_time
        
        response = {
            "id": f"chatcmpl-{uuid.uuid4().hex[:8]}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_text
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(user_message.split()),
                "completion_tokens": len(response_text.split()),
                "total_tokens": len(user_message.split()) + len(response_text.split())
            },
            # Metadados extras
            "fine_tuned": used_fine_tuned,
            "domain": domain_used,
            "confidence": confidence,
            "response_time": response_time
        }
        
        return response
        
    except Exception as e:
        print(f"❌ Erro no chat_completions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/completions") 
async def chat_completions_alias(request: ChatCompletionRequest):
    """Alias para compatibilidade"""
    return await chat_completions(request)

def generate_fallback_response(message: str) -> str:
    """Gerar resposta padrão quando fine-tuning não funcionar"""
    message_lower = message.lower()
    
    # Respostas básicas baseadas em keywords
    if any(word in message_lower for word in ['cancelar', 'pedido', 'compra']):
        return "Para cancelar seu pedido, acesse a área do cliente em nosso site ou entre em contato com nosso suporte."
    
    elif any(word in message_lower for word in ['entrega', 'prazo', 'quando']):
        return "Os prazos de entrega variam conforme sua localização e o produto. Consulte as informações na página do produto."
    
    elif any(word in message_lower for word in ['troca', 'defeito', 'problema']):
        return "Para trocas ou produtos com defeito, entre em contato com nosso suporte através do chat ou email."
    
    elif any(word in message_lower for word in ['parcelar', 'pagamento', 'juros']):
        return "Oferecemos parcelamento em cartão de crédito. Consulte as opções disponíveis no checkout."
    
    elif any(word in message_lower for word in ['api', 'erro', 'bug', '500']):
        return "Para problemas técnicos, verifique os logs do sistema e entre em contato com o suporte técnico."
    
    else:
        return "Olá! Como posso ajudá-lo? Estou aqui para responder suas dúvidas sobre nossos produtos e serviços."

if __name__ == "__main__":
    uvicorn.run("api_with_finetuning:app", host="0.0.0.0", port=5001, reload=True)
