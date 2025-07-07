import os
from core.memory import embed_brain
from interfaces.cli_chat import start_chat
from config.settings import PDF_PATH, VECTOR_DB_DIR

print('Jarvis ready')

def ensure_memory():
    if not os.path.exists(VECTOR_DB_DIR) or not os.listdir(VECTOR_DB_DIR):
        print(f"[🧠] No vector memory found. Embedding: {PDF_PATH}")
        embed_brain(PDF_PATH)
    else:
        print("[🧠] Vector memory already present. Skipping embedding.")

if __name__ == "__main__":
    ensure_memory()
    start_chat()