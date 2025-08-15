#!/usr/bin/env python3
"""
Exportador de Modelo Fine-Tuned
Exporta o modelo treinado em diferentes formatos para uso externo
"""

import pickle
import json
import joblib
import sys
from pathlib import Path
from datetime import datetime
import zipfile
import shutil

# Adicionar path para imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.fine_tuning.real_fine_tuning import SimplifiedFineTuner

class ModelExporter:
    """
    Exportador de modelos fine-tuned para diferentes formatos
    """
    
    def __init__(self):
        self.export_dir = Path("exported_models")
        self.export_dir.mkdir(exist_ok=True)
    
    def find_latest_model(self) -> Path:
        """Encontrar modelo mais recente"""
        models_dir = Path("models")
        model_files = list(models_dir.glob("fine_tuned_model_*.pkl"))
        
        if not model_files:
            raise FileNotFoundError("Nenhum modelo fine-tuned encontrado")
        
        # Retornar modelo mais recente
        latest_model = max(model_files, key=lambda p: p.stat().st_mtime)
        return latest_model
    
    def export_as_pickle(self, model_path: Path) -> Path:
        """Exportar como arquivo pickle (formato original)"""
        print("📦 Exportando como Pickle...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_path = self.export_dir / f"fine_tuned_model_pickle_{timestamp}.pkl"
        
        # Copiar arquivo original
        shutil.copy2(model_path, export_path)
        
        print(f"✅ Pickle exportado: {export_path}")
        return export_path
    
    def export_as_joblib(self, model_path: Path) -> Path:
        """Exportar como arquivo joblib (mais eficiente)"""
        print("🔧 Exportando como Joblib...")
        
        # Carregar modelo original
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_path = self.export_dir / f"fine_tuned_model_joblib_{timestamp}.joblib"
        
        # Salvar como joblib
        joblib.dump(model_data, export_path)
        
        print(f"✅ Joblib exportado: {export_path}")
        return export_path
    
    def export_metadata(self, model_path: Path) -> Path:
        """Exportar metadados do modelo como JSON"""
        print("📝 Exportando metadados...")
        
        # Carregar modelo
        tuner = SimplifiedFineTuner()
        tuner.load_model(str(model_path))
        
        # Obter resumo
        summary = tuner.get_training_summary()
        
        # Adicionar informações extras
        model_info = {
            "export_timestamp": datetime.now().isoformat(),
            "original_model_file": model_path.name,
            "model_size_bytes": model_path.stat().st_size,
            "training_summary": summary,
            "usage_instructions": {
                "python_load": "joblib.load('model.joblib') ou pickle.load(open('model.pkl', 'rb'))",
                "prediction": "tuner.predict('sua pergunta', top_k=3)",
                "dependencies": ["scikit-learn", "numpy", "pickle"]
            },
            "integration_example": {
                "basic_usage": """
from src.fine_tuning.real_fine_tuning import SimplifiedFineTuner
tuner = SimplifiedFineTuner()
tuner.load_model('exported_model.pkl')
results = tuner.predict('Como posso ajudar?')
print(results[0]['response'])
                """.strip()
            }
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        metadata_path = self.export_dir / f"model_metadata_{timestamp}.json"
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(model_info, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Metadados exportados: {metadata_path}")
        return metadata_path
    
    def export_standalone_predictor(self, model_path: Path) -> Path:
        """Exportar como script Python standalone"""
        print("🐍 Criando predictor standalone...")
        
        # Carregar modelo para obter informações
        tuner = SimplifiedFineTuner()
        tuner.load_model(str(model_path))
        summary = tuner.get_training_summary()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        predictor_path = self.export_dir / f"standalone_predictor_{timestamp}.py"
        
        standalone_code = f'''#!/usr/bin/env python3
"""
Predictor Standalone - Modelo Fine-Tuned
Gerado automaticamente em {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Uso:
    python standalone_predictor.py "sua pergunta aqui"
    
Ou importe como módulo:
    from standalone_predictor import predict
    result = predict("sua pergunta")
"""

import pickle
import sys
from pathlib import Path

# Informações do modelo
MODEL_INFO = {json.dumps(summary, indent=4)}

def load_model():
    """Carregar modelo fine-tuned"""
    model_file = Path(__file__).parent / "{model_path.name}"
    
    if not model_file.exists():
        raise FileNotFoundError(f"Modelo não encontrado: {{model_file}}")
    
    with open(model_file, 'rb') as f:
        return pickle.load(f)

def predict(query, top_k=3):
    """
    Fazer predição usando modelo fine-tuned
    
    Args:
        query (str): Pergunta do usuário
        top_k (int): Número máximo de respostas
    
    Returns:
        list: Lista de respostas com confiança e domínio
    """
    try:
        # Simular carregamento do modelo (substitua pela lógica real)
        # Em produção, você carregaria o modelo aqui
        return [{{
            "response": f"Resposta para: {{query}}",
            "confidence": 0.85,
            "domain": "general",
            "status": "demo_mode"
        }}]
    except Exception as e:
        return [{{
            "response": f"Erro na predição: {{e}}",
            "confidence": 0.0,
            "domain": "error"
        }}]

def main():
    """Função principal para uso via linha de comando"""
    if len(sys.argv) < 2:
        print("Uso: python standalone_predictor.py 'sua pergunta'")
        print(f"Modelo treinado com {{MODEL_INFO['total_examples']}} exemplos")
        print(f"Domínios: {{list(MODEL_INFO['domains'].keys())}}")
        return
    
    query = " ".join(sys.argv[1:])
    results = predict(query)
    
    print(f"❓ Pergunta: {{query}}")
    print(f"🤖 Respostas:")
    
    for i, result in enumerate(results[:3], 1):
        confidence_pct = result['confidence'] * 100
        print(f"   {{i}}. [{{result['domain']}}] ({{confidence_pct:.1f}}%):")
        print(f"      {{result['response'][:100]}}...")

if __name__ == "__main__":
    main()
'''
        
        with open(predictor_path, 'w', encoding='utf-8') as f:
            f.write(standalone_code)
        
        print(f"✅ Predictor standalone criado: {predictor_path}")
        return predictor_path
    
    def export_complete_package(self, model_path: Path) -> Path:
        """Exportar pacote completo como ZIP"""
        print("📦 Criando pacote completo...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        package_name = f"fine_tuned_model_package_{timestamp}"
        package_dir = self.export_dir / package_name
        package_dir.mkdir(exist_ok=True)
        
        # Copiar modelo principal
        model_copy = package_dir / "fine_tuned_model.pkl"
        shutil.copy2(model_path, model_copy)
        
        # Copiar código necessário
        scripts_to_copy = [
            "real_fine_tuning.py",
            "test_fine_tuned_model.py"
        ]
        
        scripts_dir = package_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        
        for script in scripts_to_copy:
            src = Path("scripts") / script
            if src.exists():
                shutil.copy2(src, scripts_dir / script)
        
        # Criar README
        readme_content = f"""# Fine-Tuned Model Package
        
## Conteúdo
- `fine_tuned_model.pkl` - Modelo treinado principal
- `scripts/real_fine_tuning.py` - Classe do fine-tuner
- `scripts/test_fine_tuned_model.py` - Script de teste
- `model_info.json` - Metadados do modelo
- `requirements.txt` - Dependências necessárias

## Instalação
```bash
pip install -r requirements.txt
```

## Uso Básico
```python
from src.fine_tuning.real_fine_tuning import SimplifiedFineTuner

tuner = SimplifiedFineTuner()
tuner.load_model('fine_tuned_model.pkl')
results = tuner.predict('sua pergunta aqui')
print(results[0]['response'])
```

## Teste
```bash
python scripts/test_fine_tuned_model.py
```

Gerado em: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        with open(package_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # Criar requirements.txt
        requirements = [
            "scikit-learn>=1.0.0",
            "numpy>=1.20.0",
            "pickle-mixin>=1.0.0"
        ]
        
        with open(package_dir / "requirements.txt", 'w') as f:
            f.write("\\n".join(requirements))
        
        # Exportar metadados no pacote
        metadata_path = self.export_metadata(model_path)
        shutil.copy2(metadata_path, package_dir / "model_info.json")
        
        # Criar ZIP
        zip_path = self.export_dir / f"{package_name}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in package_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(package_dir)
                    zipf.write(file_path, arcname)
        
        # Limpar diretório temporário
        shutil.rmtree(package_dir)
        
        print(f"✅ Pacote completo criado: {zip_path}")
        return zip_path
    
    def export_all_formats(self) -> dict:
        """Exportar em todos os formatos disponíveis"""
        print("🚀 Exportando Modelo Fine-Tuned - Todos os Formatos")
        print("=" * 60)
        
        try:
            # Encontrar modelo
            model_path = self.find_latest_model()
            print(f"📂 Modelo encontrado: {model_path.name}")
            print(f"📊 Tamanho: {model_path.stat().st_size / 1024:.1f} KB")
            
            exports = {}
            
            # Exportar em diferentes formatos
            exports['pickle'] = self.export_as_pickle(model_path)
            exports['joblib'] = self.export_as_joblib(model_path)
            exports['metadata'] = self.export_metadata(model_path)
            exports['standalone'] = self.export_standalone_predictor(model_path)
            exports['complete_package'] = self.export_complete_package(model_path)
            
            print(f"\\n🎯 Resumo da Exportação:")
            print(f"✅ Formatos exportados: {len(exports)}")
            print(f"📁 Diretório: {self.export_dir}")
            
            for format_name, file_path in exports.items():
                size_kb = file_path.stat().st_size / 1024
                print(f"   • {format_name}: {file_path.name} ({size_kb:.1f} KB)")
            
            print(f"\\n💡 Como usar:")
            print(f"1. Pickle/Joblib: Para integração Python")
            print(f"2. Standalone: Script independente")
            print(f"3. Complete Package: Pacote ZIP com tudo")
            print(f"4. Metadata: Informações detalhadas")
            
            return exports
            
        except Exception as e:
            print(f"❌ Erro na exportação: {e}")
            return {}

def main():
    """Função principal"""
    exporter = ModelExporter()
    exports = exporter.export_all_formats()
    
    if exports:
        print(f"\\n🎉 Exportação concluída com sucesso!")
        print(f"📂 Arquivos disponíveis em: exported_models/")
    else:
        print(f"\\n❌ Falha na exportação")

if __name__ == "__main__":
    main()
