from core.llm_setup import load_retrieval_chain
from core.logger import log_conversation

def start_chat():
    print("👑 Welcome to Monarch — your personal agent!")
    print("Type your question or 'exit' to quit.\n")

    qa = load_retrieval_chain()

    while True:
        try:
            query = input("You: ").strip()
            if query.lower() in ['exit', 'quit', 'bye']:
                farewell = qa.invoke("Say goodbye as if you're going to sleep.")["result"]
                print(f"Monarch: {farewell}")
                log_conversation(query, farewell)
                break

            response = qa.invoke(query)["result"]
            print(f"Monarch: {response}")
            log_conversation(query, response)
        except KeyboardInterrupt:
            print("\n[⚠️] Interrupted. Exiting...")
            break
