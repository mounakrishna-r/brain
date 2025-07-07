import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# Config
PROJECT_ROOT = "."  # Root of your repo
MEMORY_DIR = "code_memory"  # Where vector DB will be stored
EMBED_MODEL = "all-MiniLM-L6-v2"

# Step 1: Collect all .py files
def collect_python_files(root):
    py_files = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(".py") and "venv" not in dirpath and "__pycache__" not in dirpath:
                full_path = os.path.join(dirpath, filename)
                py_files.append(full_path)
    return py_files

# Step 2: Load + chunk each file
def load_and_split_files(file_paths):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    all_chunks = []

    for path in file_paths:
        try:
            loader = TextLoader(path)
            docs = loader.load()
            chunks = splitter.split_documents(docs)
            for chunk in chunks:
                chunk.metadata['source'] = path
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"Failed to load {path}: {e}")

    return all_chunks

# Step 3: Embed + store in Chroma
def embed_to_chroma(docs, persist_path=MEMORY_DIR):
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectordb = Chroma.from_documents(docs, embedding=embeddings, persist_directory=persist_path)
    vectordb.persist()
    print(f"[✓] Indexed {len(docs)} chunks into {persist_path}")

if __name__ == "__main__":
    print("[→] Scanning project files...")
    py_files = collect_python_files(PROJECT_ROOT)
    print(f"[✓] Found {len(py_files)} Python files")

    print("[→] Chunking and embedding code...")
    chunks = load_and_split_files(py_files)

    print("[→] Saving to vector memory...")
    embed_to_chroma(chunks)