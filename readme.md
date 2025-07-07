# Monarch Assistant

This version contains only your existing working logic.
# config/settings.py

PDF_PATH = "knowledge/brain.pdf"
VECTOR_DB_DIR = "virus_memory"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
# Placeholder for llm_selector.py

# core/llm_setup.py

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
# core/logger.py (Updated)

import os
import json
import csv
from datetime import datetime

LOG_FILE = "data/memory_log.json"
os.makedirs("data", exist_ok=True)

def log_conversation(user_input, response):
log_entry = {
"timestamp": datetime.now().isoformat(),
"user_input": user_input,
"virus_response": response
}

    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                data = json.load(f)
        else:
            data = []
    except json.JSONDecodeError:
        data = []

    data.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def clear_log():
with open(LOG_FILE, "w") as f:
json.dump([], f)
print(f"[🧹] Cleared: {LOG_FILE}")

def export_log_to_csv(csv_path="data/memory_log.csv"):
if not os.path.exists(LOG_FILE):
print("[!] No log file to export.")
return

    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["timestamp", "user_input", "virus_response"])
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

    print(f"[📁] Log exported to: {csv_path}")
# core/memory.py

import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from config.settings import EMBED_MODEL_NAME, VECTOR_DB_DIR

# Common chunker
def chunk_documents(docs, chunk_size=500, overlap=50):
splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
return splitter.split_documents(docs)

# PDF embedding
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

# Codebase embedding
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

# Alias used in main.py
def embed_brain(pdf_path, persist_path=VECTOR_DB_DIR):
embed_pdf(pdf_path, persist_path)
# Placeholder for tools.py

data/memory_log.json
[
{
"timestamp": "2025-06-28T18:24:22.790880",
"user_input": "Hi, How are you?",
"virus_response": " I'm an AI, so I don't have feelings, but I'm functioning well and ready to help you with your questions! If you have any questions or need assistance, feel free to ask."
},
{
"timestamp": "2025-06-28T18:24:36.331228",
"user_input": "exit",
"virus_response": " The term \"exit\" can have several meanings depending on the context. In programming or computer science, it refers to a command or function that closes or quits a program. In a more general sense, it could refer to leaving a place (physical or virtual), ending an activity, or terminating a process. Without specific additional context, it's difficult to provide a precise answer."
},
{
"timestamp": "2025-06-28T18:25:47.568385",
"user_input": "exit",
"virus_response": " As I am not a physical entity, I don't have the ability to turn myself off or go to sleep. However, if we continue with the metaphor, I would \"go offline\" temporarily. Goodnight!"
},
{
"timestamp": "2025-06-28T18:26:28.522917",
"user_input": "exit",
"virus_response": " Alright, it seems like we're wrapping up our conversation. I hope this chat has been helpful to you. If you have any more questions or need further assistance in the future, feel free to reach out again! Goodnight and take care."
},
{
"timestamp": "2025-06-28T18:27:36.072639",
"user_input": "exit",
"virus_response": " I'm simulating the end of our conversation by saying goodnight and going to \"sleep.\" Good night! It was great interacting with you. If you need anything else, don't hesitate to reach out again. Take care and have a wonderful day!"
},
{
"timestamp": "2025-06-28T18:31:45.753010",
"user_input": "hi",
"virus_response": " Hello! How can I help you today?"
},
{
"timestamp": "2025-06-28T18:31:52.061533",
"user_input": "bye",
"virus_response": " Alright, it seems like we've reached the end of our conversation for now. I'll \"turn off\" or exit this program until we can chat again. Until then, take care and have a great day!"
},
{
"timestamp": "2025-06-28T18:46:26.911583",
"user_input": "hii",
"virus_response": " Hello! How can I help you today?"
},
{
"timestamp": "2025-06-28T18:46:44.781459",
"user_input": "what is \"the\" used for",
"virus_response": " The term \"the\" is a definite article in English language. It is used before a noun when we are referring to something specific or known to both speaker and listener. For example, \"I saw the cat on the mat.\" Here, \"the cat\" refers to a specific cat that has been previously mentioned or known by the listener."
},
{
"timestamp": "2025-06-28T18:46:53.001533",
"user_input": "bye",
"virus_response": " I'm glad we had this conversation! It seems like we're reaching the end, much like turning off a device or going to sleep. Until we meet again, take care and have a fantastic day!"
},
{
"timestamp": "2025-06-29T16:47:44.084010",
"user_input": "good afternoon",
"virus_response": " Good afternoon!"
},
{
"timestamp": "2025-06-29T16:48:11.609095",
"user_input": "what is up?",
"virus_response": " In the provided context, there's no clear information about the meaning of \"up\". However, in everyday language, \"what's up?\" is often used as a casual greeting or question asking about someone's current activities or well-being."
},
{
"timestamp": "2025-06-29T16:49:09.173976",
"user_input": "bye",
"virus_response": " Alright, it seems like we've reached the end of our conversation for now. I'll be \"turning off\" or closing down, much like a device would when it goes to sleep. Until next time! Take care and I look forward to speaking with you again soon."
}
]

# dev_utils/injector.py

import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROJECT_MAP_FILE = "dev_utils/project_map.json"
LOG_FILE = "logs/injector_log.json"
os.makedirs("logs", exist_ok=True)

def log_injection(instruction, file_path, summary="Change applied"):
entry = {
"timestamp": datetime.now().isoformat(),
"instruction": instruction,
"file_modified": file_path,
"summary": summary
}

    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                log = json.load(f)
        except json.JSONDecodeError:
            log = []
    else:
        log = []

    log.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

def choose_file_with_gpt(instruction):
with open(PROJECT_MAP_FILE, "r") as f:
project_map = json.load(f)

    prompt = f"""
Instruction:
"{instruction}"

Files and roles:
{json.dumps(project_map, indent=2)}

Return ONLY the best file path to modify.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a smart code assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip().strip('"')

def inject_feature(instruction, model="gpt-4"):
print("[→] Choosing target file...")
file_path = choose_file_with_gpt(instruction)

    if not os.path.exists(file_path):
        print(f"[✗] File not found: {file_path}")
        return

    with open(file_path, "r") as f:
        original = f.read()

    prompt = f"""
You are a helpful AI that modifies Python files based on user instructions.

Instruction:
{instruction}

Original code:
{original}
"""

    print("[→] Sending to GPT...")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an autonomous coding agent. Return the updated full file only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=3000
    )

    updated = response.choices[0].message.content.strip()

    backup = file_path + ".bak"
    if os.path.exists(backup):
        os.remove(backup)
    os.rename(file_path, backup)

    with open(file_path, "w") as f:
        f.write(updated)

    print(f"[✓] Updated: {file_path} (backup saved)")
    log_injection(instruction, file_path)

# Optional test run
if __name__ == "__main__":
test_instruction = "Add a function to clear the memory_log.json file"
inject_feature(test_instruction)
dev_utils/project_map.json
{
"injector.py": "Handles intelligent code injection and modification",
"chat.py": "Manages the assistant's interactive chat loop",
"embedder.py": "Embeds documents into vector memory",
"main.py": "Launches the assistant and chat",
"project_indexer.py": "Indexes code files and creates searchable embeddings",
"readme.md": "Contains project overview and instructions for users"
}
# interfaces/cli_chat.py

from core.llm_setup import load_retrieval_chain
from core.logger import log_conversation

def start_chat():
print("🧠 Welcome to the Monarch CLI Assistant!")
print("Type your question or 'exit' to quit.\n")

    qa = load_retrieval_chain()

    while True:
        try:
            query = input("You: ").strip()
            if query.lower() in ['exit', 'quit', 'bye']:
                farewell = qa.run("Say goodbye as if you're going to sleep.")
                print(f"Monarch: {farewell}")
                log_conversation(query, farewell)
                break

            response = qa.run(query)
            print(f"Monarch: {response}")
            log_conversation(query, response)
        except KeyboardInterrupt:
            print("\n[⚠️] Interrupted. Exiting...")
            break

logs/injector_logs.json
[
{
"timestamp": "2025-06-29T20:27:09.795033",
"instruction": "Add a raad me document to project root, this document will be kept on modified and added and carried along the path, so have a good plan on how to write it",
"file_modified": "project_indexer.py",
"summary": "Change applied"
},
{
"timestamp": "2025-06-29T20:35:25.821496",
"instruction": "Add a read me to the project with instructions on how to use it and how to contribute.",
"file_modified": "readme.md",
"summary": "Change applied"
}
]
#tests/test.py

from dev_utils.injector import inject_feature

inject_feature("Add a read me to the project with instructions on how to use it and how to contribute.")
# tests/test_virus_alive.py

from core.llm_setup import load_retrieval_chain

def test_basic_response():
qa = load_retrieval_chain()
query = "What is your purpose?"
response = qa.run(query)

    assert isinstance(response, str)
    assert any(word in response.lower() for word in ["assist", "help", "answer", "support"])

    print("[✓] Monarch assistant is responsive and coherent.")

if __name__ == "__main__":
test_basic_response()
# main.py

import os
from core.memory import embed_brain
from interfaces.cli_chat import start_chat
from config.settings import PDF_PATH, VECTOR_DB_DIR

def ensure_memory():
if not os.path.exists(VECTOR_DB_DIR) or not os.listdir(VECTOR_DB_DIR):
print(f"[🧠] No vector memory found. Embedding: {PDF_PATH}")
embed_brain(PDF_PATH)
else:
print("[🧠] Vector memory already present. Skipping embedding.")

if __name__ == "__main__":
ensure_memory()
start_chat()
