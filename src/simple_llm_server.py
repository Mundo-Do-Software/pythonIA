#!/usr/bin/env python3
"""
Servidor de Chat API simples usando Ollama como backend
Compatível com OpenAI API para uso com N8N
Suporte a requisições concorrentes com cache Redis semântico
"""
import os
import time
import uuid
import asyncio
import aiohttp
import hashlib
import json
import numpy as np
import redis.asyncio as redis
from typing import List, Optional, Dict, Any
from datetime import datetime
from sentence_transformers import SentenceTransformer

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import requests

# Configuração Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))  # TTL configurável (padrão 5 min)

# Modelos de dados para API compatível com OpenAI
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = "deepseek-coder:1.3b"  # Modelo padrão DeepSeek 1.3B
    messages: List[ChatMessage]
    temperature: float = 0.7
    max_tokens: int = 512
    stream: bool = False

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]

# Configurações globais
API_KEY = os.getenv("API_KEY", "dfdjhasdfgldfugydlsuiflhgd")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")  # Ollama configurável via env

# Carregar modelo fine-tuned se disponível
fine_tuned_model = None
try:
    import sys
    from pathlib import Path
    
    # Adicionar path para importar módulos de fine-tuning
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    sys.path.insert(0, str(project_root))
    
    # Verificar se existe modelo fine-tuned
    fine_tuned_path = current_dir / "current_fine_tuned_model.pkl"
    if fine_tuned_path.exists():
        from src.fine_tuning.real_fine_tuning import SimplifiedFineTuner
        fine_tuned_model = SimplifiedFineTuner()
        if fine_tuned_model.load_model(str(fine_tuned_path)):
            print(f"✅ Modelo fine-tuned carregado: {fine_tuned_path}")
        else:
            fine_tuned_model = None
            print(f"❌ Falha ao carregar modelo fine-tuned")
    else:
        print(f"ℹ️  Nenhum modelo fine-tuned encontrado, usando apenas Ollama")
except Exception as e:
    print(f"⚠️  Erro ao carregar modelo fine-tuned: {e}")
    fine_tuned_model = None

# Inicializar FastAPI
app = FastAPI(title="Simple LLM API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def check_ollama():
    """Verifica se o Ollama está disponível"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def try_fine_tuned_response(prompt: str) -> dict:
    """Tenta obter resposta do modelo fine-tuned primeiro"""
    global fine_tuned_model
    
    if fine_tuned_model is None:
        return None
    
    try:
        # Usar o modelo fine-tuned para gerar resposta
        results = fine_tuned_model.predict(prompt, top_k=1)
        
        if results and len(results) > 0:
            best_result = results[0]
            confidence = best_result.get('confidence', 0)
            
            # Só usar fine-tuned se confiança for razoável (>0.2)
            if confidence > 0.2:
                return {
                    "response": best_result.get('response', ''),
                    "domain": best_result.get('domain', 'unknown'),
                    "confidence": confidence,
                    "fine_tuned": True
                }
    except Exception as e:
        print(f"⚠️  Erro no modelo fine-tuned: {e}")
    
    return None

def format_messages_for_ollama(messages: List[ChatMessage]) -> str:
    """Formata mensagens para o Ollama"""
    formatted = ""
    
    for msg in messages:
        if msg.role == "system":
            formatted += f"System: {msg.content}\n\n"
        elif msg.role == "user":
            formatted += f"User: {msg.content}\n\n"
        elif msg.role == "assistant":
            formatted += f"Assistant: {msg.content}\n\n"
    
    return formatted.strip()

# Cliente Redis global e modelo de embeddings
redis_client = None
embedding_model = None

async def init_redis():
    """Inicializa conexão Redis e modelo de embeddings"""
    global redis_client, embedding_model
    try:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        await redis_client.ping()
        print(f"🟢 [REDIS] Conectado ao Redis em {REDIS_URL}")
        
        # Inicializar modelo de embeddings (leve e rápido)
        print("🧠 [EMBEDDINGS] Carregando modelo semântico...")
        embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        print("✅ [EMBEDDINGS] Modelo semântico carregado")
        
    except Exception as e:
        print(f"🔴 [INIT] Erro ao inicializar: {e}")
        redis_client = None
        embedding_model = None

def cosine_similarity(a, b):
    """Calcula similaridade cosseno entre dois vetores"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_cache_key(prompt: str, model: str) -> str:
    """Gera chave do cache baseada no prompt e modelo"""
    content = f"{model}:{prompt}"
    return f"llm_cache:{hashlib.md5(content.encode()).hexdigest()}"

def get_embedding_key(prompt: str) -> str:
    """Gera chave para o embedding do prompt"""
    return f"embedding:{hashlib.md5(prompt.encode()).hexdigest()}"

async def find_similar_cached_response(prompt: str, model: str, similarity_threshold: float = 0.85) -> Optional[str]:
    """Busca resposta semanticamente similar no cache Redis"""
    if not redis_client or not embedding_model:
        return None
    
    try:
        # Gerar embedding da pergunta atual
        current_embedding = embedding_model.encode(prompt)
        
        # Buscar todas as chaves de embedding
        embedding_keys = await redis_client.keys("embedding:*")
        
        best_match = None
        best_similarity = 0.0
        
        print(f"🔍 [SEMANTIC SEARCH] Buscando entre {len(embedding_keys)} perguntas armazenadas...")
        
        for emb_key in embedding_keys:
            try:
                # Recuperar embedding armazenado
                stored_data = await redis_client.get(emb_key)
                if not stored_data:
                    continue
                    
                stored_info = json.loads(stored_data)
                if stored_info.get("model") != model:
                    continue
                
                stored_embedding = np.array(stored_info["embedding"])
                
                # Calcular similaridade
                similarity = cosine_similarity(current_embedding, stored_embedding)
                
                if similarity > best_similarity and similarity >= similarity_threshold:
                    best_similarity = similarity
                    best_match = {
                        "cache_key": stored_info["cache_key"],
                        "similarity": similarity,
                        "original_prompt": stored_info["prompt"]
                    }
                    
            except Exception as e:
                print(f"⚠️ [SEMANTIC] Erro ao processar {emb_key}: {e}")
                continue
        
        if best_match:
            # Buscar resposta no cache
            try:
                cached_data = await redis_client.get(best_match["cache_key"])
                if cached_data:
                    cache_info = json.loads(cached_data)
                    print(f"🎯 [SEMANTIC HIT] Similaridade: {best_similarity:.3f}")
                    print(f"📝 [SIMILAR TO] '{best_match['original_prompt'][:50]}...'")
                    return cache_info["response"]
            except Exception as e:
                print(f"🔴 [SEMANTIC] Erro ao recuperar resposta: {e}")
        
        print(f"❌ [SEMANTIC MISS] Nenhuma pergunta similar encontrada (threshold: {similarity_threshold})")
        return None
        
    except Exception as e:
        print(f"🔴 [SEMANTIC] Erro na busca semântica: {e}")
        return None

def is_valid_response(response: str) -> bool:
    """Verifica se a resposta é válida (não é erro ou timeout)"""
    error_indicators = [
        "Timeout na requisição",
        "Erro na chamada do Ollama",
        "Erro ao conectar com Ollama",
        "HTTPConnectionPool",
        "Connection refused",
        "Read timed out",
        "404",
        "500",
        "502",
        "503"
    ]
    
    # Verificar se contém indicadores de erro
    for indicator in error_indicators:
        if indicator in response:
            return False
    
    # Verificar se a resposta é muito curta (provavelmente erro)
    if len(response.strip()) < 10:
        return False
        
    return True

async def cache_response_with_embedding(prompt: str, model: str, response: str):
    """Armazena resposta no cache Redis com embedding para busca semântica - apenas se for uma resposta válida"""
    print(f"🔥🔥🔥 [CACHE_FUNCTION] CHAMADA! Resposta: '{response[:30]}...'")
    
    if not redis_client or not embedding_model:
        print(f"🔥🔥🔥 [CACHE_FUNCTION] Redis ou embedding não disponível")
        return
    
    # ✅ VALIDAÇÃO: Só armazenar respostas válidas no cache
    is_valid = is_valid_response(response)
    print(f"🔍 [VALIDATION] Resposta: '{response[:50]}...'")
    print(f"🔍 [VALIDATION] É válida: {is_valid}")
    
    if not is_valid:
        print(f"⚠️ [CACHE SKIP] Resposta inválida não será armazenada!")
        return
    
    try:
        # Cache da resposta (tradicional)
        cache_key = get_cache_key(prompt, model)
        cache_data = {
            "response": response,
            "timestamp": time.time(),
            "prompt": prompt,
            "model": model
        }
        await redis_client.setex(cache_key, CACHE_TTL, json.dumps(cache_data))
        
        # Armazenar embedding para busca semântica
        embedding_key = get_embedding_key(prompt)
        current_embedding = embedding_model.encode(prompt)
        
        embedding_data = {
            "embedding": current_embedding.tolist(),
            "prompt": prompt,
            "model": model,
            "cache_key": cache_key,
            "timestamp": time.time()
        }
        await redis_client.setex(embedding_key, CACHE_TTL, json.dumps(embedding_data))
        
        print(f"💾 [SEMANTIC CACHE] Resposta válida armazenada")
        
    except Exception as e:
        print(f"🔴 [SEMANTIC] Erro ao armazenar: {e}")

def select_best_model(messages: List[ChatMessage], requested_model: str = "auto") -> str:
    """Seleciona o melhor modelo DeepSeek baseado no contexto"""
    if requested_model != "auto":
        return requested_model
    
    # Análise rápida do conteúdo
    content = " ".join([msg.content.lower() for msg in messages]) if messages else ""
    
    # Palavras-chave para modelo robusto (6.7B)
    complex_keywords = [
        "analise", "análise", "financeiro", "estrategia", "estratégia",
        "diagnostico", "diagnóstico", "motor", "mecânico", "complexo",
        "detalhado", "explicação", "explicacao", "tutorial", "passo a passo",
        "desenvolvimento", "programação", "programacao", "código", "codigo",
        "arquitetura", "design", "planejamento", "relatório", "relatorio"
    ]
    
    # Critérios para usar DeepSeek 6.7B (modelo mais robusto)
    use_large_model = (
        any(kw in content for kw in complex_keywords) or  # Palavras complexas
        len(content) > 150 or  # Texto longo
        content.count("?") > 1 or  # Múltiplas perguntas
        "como fazer" in content or  # Tutoriais
        "explique" in content or
        "desenvolver" in content
    )
    
    if use_large_model:
        return "deepseek-coder:6.7b"
    
    # Para textos simples e respostas rápidas, usar DeepSeek 1.3B
    return "deepseek-coder:1.3b"

async def call_ollama_async(prompt: str, model: str = "deepseek-coder:1.3b", temperature: float = 0.7, max_tokens: int = 512) -> str:
    """Chama o Ollama de forma assíncrona com otimizações para modelos DeepSeek"""
    try:
        print(f"🔥 [ASYNC] Chamando Ollama com modelo: {model}")
        
        # Parâmetros otimizados para modelos DeepSeek
        base_options = {
            "temperature": temperature,
            "num_predict": max_tokens,
            "repeat_penalty": 1.1,
            "top_k": 40,
            "top_p": 0.9,
            "repeat_last_n": 64,
            "penalize_newline": False,
        }
        
        # Configurações específicas por modelo
        if "1.3b" in model.lower():
            # DeepSeek 1.3B - otimizado para velocidade
            options = {
                **base_options,
                "num_ctx": 2048,      # Contexto menor para velocidade
                "num_batch": 512,     # Batch size para modelos pequenos
                "num_thread": 6,      # Menos threads para modelo pequeno
            }
        elif "6.7b" in model.lower():
            # DeepSeek 6.7B - otimizado para qualidade
            options = {
                **base_options,
                "num_ctx": 4096,      # Contexto maior para melhor qualidade
                "num_batch": 256,     # Batch menor para modelo grande
                "num_thread": 8,      # Mais threads para modelo grande
            }
        else:
            # Configuração padrão para outros modelos
            options = {
                **base_options,
                "num_ctx": 2048,
                "num_batch": 512,
                "num_thread": 8,
            }
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": options
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{OLLAMA_URL}/api/generate",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=180)  # Timeout aumentado para 3 minutos
            ) as response:
                
                print(f"🌐 [ASYNC] Status da resposta: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    return result.get("response", "").strip()
                else:
                    error_text = await response.text()
                    print(f"❌ [ASYNC] Erro HTTP: {error_text}")
                    return f"Erro na chamada do Ollama: {response.status}"
                    
    except asyncio.TimeoutError:
        print(f"⏰ [ASYNC] Timeout na requisição para modelo {model}")
        return f"Timeout na requisição para o modelo {model}"
    except Exception as e:
        print(f"❌ [ASYNC] Exceção: {e}")
        return f"Erro ao conectar com Ollama: {str(e)}"

def call_ollama(prompt: str, model: str = "deepseek-coder:1.3b", temperature: float = 0.7, max_tokens: int = 512) -> str:
    """Versão síncrona mantida para compatibilidade com modelos DeepSeek"""
    try:
        print(f"🔥 Chamando Ollama com modelo: {model}")
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=180
        )
        
        print(f"🌐 Status da resposta: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "").strip()
        else:
            print(f"❌ Erro HTTP: {response.text}")
            return f"Erro na chamada do Ollama: {response.status_code}"
            
    except Exception as e:
        print(f"❌ Exceção: {e}")
        return f"Erro ao conectar com Ollama: {str(e)}"

def generate_mock_response(messages: List[ChatMessage]) -> str:
    """Gera uma resposta mock quando Ollama não estiver disponível"""
    last_message = messages[-1].content if messages else "Olá"
    
    mock_responses = [
        f"Olá! Recebi sua mensagem: '{last_message}'. Este é um servidor de exemplo rodando sem GPU.",
        f"Entendi que você disse: '{last_message}'. Como posso ajudar você hoje?",
        f"Sua mensagem '{last_message}' foi recebida. Este é um servidor mock para demonstração.",
        f"Processando sua solicitação sobre: '{last_message}'. Sistema funcionando corretamente!",
    ]
    
    import random
    return random.choice(mock_responses)

@app.on_event("startup")
async def startup_event():
    """Inicializa Redis e verifica conectividade"""
    # Inicializar Redis
    await init_redis()
    
    # Verificar Ollama
    if check_ollama():
        print("✅ Ollama detectado e funcionando")
    else:
        print("⚠️ Ollama não disponível - usando respostas mock")

@app.get("/")
async def root():
    """Health check"""
    ollama_status = "connected" if check_ollama() else "mock_mode"
    return {
        "status": "running",
        "backend": ollama_status,
        "model": "deepseek-coder:1.3b" if check_ollama() else "mock",
        "models_available": ["deepseek-coder:1.3b", "deepseek-coder:6.7b"],
        "api_version": "1.0.0"
    }

@app.get("/v1/models")
async def list_models():
    """Lista modelos disponíveis (compatível com OpenAI)"""
    available_models = []
    
    # Verificar quais modelos estão instalados no Ollama
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        
        if response.status_code == 200:
            data = response.json()  
            ollama_models = data.get("models", [])
            
            for model in ollama_models:
                full_name = model["name"]
                
                # Mapear nomes para IDs limpos - com foco nos modelos DeepSeek
                if full_name == "deepseek-coder:1.3b":
                    model_id = "deepseek-1.3b"
                elif full_name == "deepseek-coder:6.7b":
                    model_id = "deepseek-6.7b"
                elif full_name == "mistral:latest":
                    model_id = "mistral"
                elif full_name == "llama3.2:3b":
                    model_id = "llama3.2"
                else:
                    # Fallback genérico
                    model_id = full_name.split(":")[0]
                
                model_entry = {
                    "id": model_id,
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "local",
                    "size": model.get("size", 0)
                }
                
                available_models.append(model_entry)
                    
    except Exception as e:
        # Fallback para modelos DeepSeek padrão
        available_models.extend([
            {
                "id": "deepseek-1.3b",
                "object": "model", 
                "created": int(time.time()),
                "owned_by": "local"
            },
            {
                "id": "deepseek-6.7b",
                "object": "model", 
                "created": int(time.time()),
                "owned_by": "local"
            }
        ])
    
    result = {
        "object": "list",
        "data": available_models
    }
    
    return result

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """Endpoint principal de chat (compatível com OpenAI)"""
    
    try:
        start_time = time.time()
        
        print(f"🔥 DEBUG: Iniciando chat_completions")
        print(f"🔥 DEBUG: request.model = '{request.model}'")
        print(f"🔥 DEBUG: Mensagens recebidas: {len(request.messages)}")
        
        # Extrair última mensagem do usuário para teste de fine-tuning
        user_message = None
        for msg in request.messages:
            if msg.role == "user":
                user_message = msg.content
        
        # 1. TENTAR MODELO FINE-TUNED PRIMEIRO
        fine_tuned_result = None
        if user_message:
            fine_tuned_result = try_fine_tuned_response(user_message)
            
        if fine_tuned_result:
            print(f"🧠 DEBUG: Usando resposta fine-tuned (confiança: {fine_tuned_result['confidence']:.3f})")
            response_text = fine_tuned_result['response']
            backend_used = f"fine-tuned-{fine_tuned_result['domain']}"
            
            # Criar resposta no formato OpenAI
            response = ChatCompletionResponse(
                id=f"chatcmpl-{uuid.uuid4().hex[:8]}",
                created=int(time.time()),
                model=request.model,
                choices=[{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_text
                    },
                    "finish_reason": "stop"
                }],
                usage={
                    "prompt_tokens": len(user_message.split()) if user_message else 0,
                    "completion_tokens": len(response_text.split()),
                    "total_tokens": len(user_message.split()) + len(response_text.split()) if user_message else len(response_text.split())
                }
            )
            
            # Adicionar metadados extras
            response_dict = response.dict()
            response_dict.update({
                "fine_tuned": True,
                "domain": fine_tuned_result['domain'],
                "confidence": fine_tuned_result['confidence'],
                "backend": backend_used,
                "response_time": time.time() - start_time
            })
            
            return response_dict
        
        # 2. FALLBACK PARA OLLAMA se fine-tuned não funcionar ou não existir
        print(f"🔥 DEBUG: Usando Ollama como fallback")
        
        if check_ollama():
            print(f"🔥 DEBUG: Ollama está disponível")
            # Selecionar modelo apropriado
            selected_model = select_best_model(request.messages, request.model)
            print(f"🔥 DEBUG: Modelo após seleção: '{selected_model}'")
            
            # Usar Ollama de forma assíncrona com cache Redis semântico
            prompt = format_messages_for_ollama(request.messages)
            print(f"🔥 DEBUG: Prompt formatado: '{prompt[:100]}...'")
            
            # Buscar cache semântico primeiro
            cached_response = await find_similar_cached_response(prompt, selected_model)
            
            if cached_response:
                response_text = cached_response
                backend_used = f"semantic-cache-{selected_model}"
            else:
                response_text = await call_ollama_async(
                    prompt, 
                    selected_model, 
                    request.temperature, 
                    request.max_tokens
                )
                # Armazenar no cache Redis com embedding
                await cache_response_with_embedding(prompt, selected_model, response_text)
                backend_used = f"ollama-{selected_model}"
        else:
            print(f"🔥 DEBUG: Ollama não disponível, usando mock")
            # Usar resposta mock
            response_text = generate_mock_response(request.messages)
            backend_used = "mock"
            selected_model = "mock"
        
        generation_time = time.time() - start_time
        
        print(f"🔤 Mensagens: {len(request.messages)} mensagem(s)")
        print(f"🤖 Modelo selecionado: {selected_model}")
        print(f"⚡ Resposta gerada em {generation_time:.2f}s usando {backend_used}")
        print(f"📝 Resposta: {response_text[:100]}...")
        
        # Criar resposta compatível com OpenAI
        completion_response = {
            "id": f"chatcmpl-{uuid.uuid4()}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.model,  # Retornar o modelo solicitado originalmente
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_text
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": sum(len(msg.content.split()) for msg in request.messages),
                "completion_tokens": len(response_text.split()),
                "total_tokens": sum(len(msg.content.split()) for msg in request.messages) + len(response_text.split())
            }
        }
        
        return completion_response
        
    except Exception as e:
        print(f"❌ Erro durante geração: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/completions")
async def chat_completions_simple(request: ChatCompletionRequest):
    """Endpoint alternativo sem /v1"""
    return await chat_completions(request)

if __name__ == "__main__":
    print("🚀 Iniciando Simple LLM Server...")
    print("🔌 Tentando conectar com Ollama...")
    
    # Configurar servidor
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        log_level="info"
    )
