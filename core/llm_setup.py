from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from config.settings import VECTOR_DB_DIR, EMBED_MODEL_NAME

def load_retrieval_chain():
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
    vectordb = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)
    llm = OllamaLLM(model="mistral")

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(search_type="similarity", k=4),
        return_source_documents=False
    )
