from core.llm_setup import load_retrieval_chain
from core.logger import log_conversation

def start_chat():
    print("🧠 Welcome to the JARVIS CLI Assistant!")
    print("Type your question or 'exit' to quit.\n")

    qa = load_retrieval_chain()

    while True:
        try:
            query = input("You: ").strip()
            if query.lower() in ['exit', 'quit', 'bye']:
                farewell = qa.run("Say goodbye as if you're going to sleep.")
                print(f"JARVIS: {farewell}")
                log_conversation(query, farewell)
                break

            response = qa.run(query)
            print(f"JARVIS: {response}")
            log_conversation(query, response)
        except KeyboardInterrupt:
            print("\n[⚠️] Interrupted. Exiting...")
            break
