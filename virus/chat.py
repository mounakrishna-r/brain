from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
import json
import os
from datetime import datetime
import random

def load_virus_chat(persist_path="virus_memory"):

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma(persist_directory=persist_path, embedding_function=embeddings)

    llm = OllamaLLM(model="mistral")

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(search_type="similarity",k=4),
        return_source_documents=False
    )
    return qa_chain

def start_chat():
    print("Welcome to the Virus Chatbot! Type 'exit' to quit.\n")
    qa = load_virus_chat()

    while True:
        query = input("You: ")
        if query.lower() in ['exit', 'quit','bye']:
            response = qa.run("Pretend you are turning off and going to sleep.This is a metaphor for the end of our conversation.")
            print("VIRUS: ",{response})
            log_conversation(query, response)
            goodbye_message()
            break

        response = qa.run(query)
        print("VIRUS: ",{response})
        log_conversation(query, response)

def log_conversation(user_input, virus_response):
    log_path = "data/memory_log.json"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "virus_response": virus_response
    }

    # Read existing log entries if file exists, else start a new list
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            try:
                log_data = json.load(f)
            except json.JSONDecodeError:
                log_data = []
    else:
        log_data = []

    log_data.append(log_entry)

    with open(log_path, "w") as f:
        json.dump(log_data, f, indent=2)

def goodbye_message():
    quotes = ["Goodbye! Remember, the only way to do great work is to love what you do. - Steve Jobs",
              "See you later! The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
              "Farewell! The best way to predict the future is to create it. - Abraham Lincoln"]
    print(random.choice(quotes))
    print("Current time: ", datetime.now().strftime("%H:%M:%S"))