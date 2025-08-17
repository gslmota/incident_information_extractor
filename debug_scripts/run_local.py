#!/usr/bin/env python3

import os
import sys
import uvicorn

os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"
os.environ["OLLAMA_MODEL"] = "tinyllama"

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def main():

    print("Iniciando Incident Information Extractor API...")
    print(f"Ollama URL: {os.environ['OLLAMA_BASE_URL']}")
    print(f"Modelo: {os.environ['OLLAMA_MODEL']}")
    print("API disponível em: http://localhost:8000")
    print("Docs disponíveis em: http://localhost:8000/docs")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "src.presentation.api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="debug",
            reload_dirs=["src"]
        )
    except KeyboardInterrupt:
        print("\nAPI interrompida pelo usuário")
    except Exception as e:
        print(f"Erro ao iniciar API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()