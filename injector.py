# injector.py (v2)
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

EMBED_MODEL = "all-MiniLM-L6-v2"
VECTOR_DB_PATH = "code_memory"

def inject_feature(instruction, model="gpt-4", top_k=1):
    print("[→] Searching for most relevant file...")

    # Step 1: Load memory
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectordb = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embeddings)
    retriever = vectordb.as_retriever(search_type="similarity", k=top_k)

    # Step 2: Retrieve most relevant code snippet
    docs = retriever.get_relevant_documents(instruction)
    if not docs:
        print("No relevant files found.")
        return

    file_path = docs[0].metadata["source"]
    print(f"[✓] Target file selected: {file_path}")

    # Step 3: Load the full file content
    with open(file_path, "r") as f:
        original_code = f.read()

    # Step 4: Build prompt for GPT
    system_prompt = (
        "You are a coding assistant inside a smart AI system. "
        "You will receive an instruction and the full content of a target code file. "
        "Apply the instruction intelligently. Output only the updated file content."
    )

    user_prompt = f"""
INSTRUCTION:
{instruction}

TARGET FILE: {file_path}

CURRENT CONTENT:
{original_code}
"""

    print("[→] Asking GPT to modify the file...")

    response = client.chat.completions.create(model=model,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.2,
    max_tokens=3000)

    updated_code = response.choices[0].message.content

    # Step 5: Backup original, overwrite file
    backup_path = file_path + ".bak"
    os.rename(file_path, backup_path)

    with open(file_path, "w") as f:
        f.write(updated_code)

    print(f"[✓] File updated: {file_path}")
    print(f"[📦] Original backed up as: {backup_path}")

def shutdown():
    print("Shutting down the assistant...")
    print("Summary: ")
    print("Files processed: ", len(vectordb))
    print("Last file updated: ", file_path)
    print("Last backup created: ", backup_path)
    exit()