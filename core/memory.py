import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from config.settings import EMBED_MODEL_NAME, VECTOR_DB_DIR

def chunk_documents(docs, chunk_size=500, overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_documents(docs)

def embed_pdf(pdf_path, persist_path=VECTOR_DB_DIR):
    print(f"[→] Loading PDF: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    chunks = chunk_documents(docs)
    print(f"[✓] PDF split into {len(chunks)} chunks.")

    embedder = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
    vectordb = Chroma.from_documents(chunks, embedding=embedder, persist_directory=persist_path)
    vectordb.persist()
    print(f"[✓] Embedded PDF stored in {persist_path}")

def embed_codebase(root_dir=".", persist_path="code_memory"):
    print(f"[→] Scanning Python files in {root_dir}...")
    py_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".py") and "venv" not in dirpath and "__pycache__" not in dirpath:
                py_files.append(os.path.join(dirpath, file))

    print(f"[✓] Found {len(py_files)} Python files.")
    all_chunks = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    for path in py_files:
        try:
            loader = TextLoader(path)
            docs = loader.load()
            chunks = splitter.split_documents(docs)
            for c in chunks:
                c.metadata['source'] = path
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"[✗] Error loading {path}: {e}")

    embedder = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
    vectordb = Chroma.from_documents(all_chunks, embedding=embedder, persist_directory=persist_path)
    vectordb.persist()
    print(f"[✓] Indexed {len(all_chunks)} code chunks into {persist_path}")

def embed_brain(pdf_path, persist_path=VECTOR_DB_DIR):
    embed_pdf(pdf_path, persist_path)
