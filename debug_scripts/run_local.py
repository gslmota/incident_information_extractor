#!/usr/bin/env python3
import os
import uvicorn

os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"
os.environ["MODEL_NAME"] = "tinyllama"

if __name__ == "__main__":
    uvicorn.run(
        "src.presentation.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True, 
        log_level="debug"
    )