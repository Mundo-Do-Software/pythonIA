# Configuração otimizada para RTX 2060 (6GB VRAM)

# Configurações específicas DeepSeek + RTX 2060
OLLAMA_RTX2060_CONFIG = {
    # Modelo otimizado para 6GB VRAM
    "recommended_model": "deepseek-coder:1.3b",  # Cabe perfeitamente na RTX 2060
    
    # Configurações de GPU
    "gpu_layers": 35,           # Otimizado para RTX 2060
    "context_length": 2048,     # Máximo para 6GB sem problemas
    "batch_size": 512,          # Equilibrio performance/memoria
    "threads": 8,               # RTX 2060 tem bom paralelismo
    
    # Configurações de memória
    "max_memory": 5500,         # Deixar ~500MB livres
    "memory_growth": True,      # Crescimento dinâmico
    "allow_growth": True,
    
    # Performance
    "flash_attention": True,
    "use_mlock": True,
    "use_mmap": True,
    "low_vram": False,          # RTX 2060 tem VRAM suficiente
    
    # Concorrência (otimizada para local)
    "max_concurrent": 1,
    "num_parallel": 1,
    "max_queue": 128,
    
    # Estimativas de performance
    "expected_tokens_per_second": 25,  # ~25 tokens/s na RTX 2060
    "warmup_time": 3,                  # 3s para primeiro token
    "memory_usage_mb": 4800,           # ~4.8GB para DeepSeek 1.3B
}

print("🎮 Configuração RTX 2060 carregada!")
print(f"💾 VRAM esperada: {OLLAMA_RTX2060_CONFIG['memory_usage_mb']}MB")
print(f"⚡ Performance: ~{OLLAMA_RTX2060_CONFIG['expected_tokens_per_second']} tokens/s")
print(f"🧠 Context: {OLLAMA_RTX2060_CONFIG['context_length']} tokens")
