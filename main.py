import os
from virus.embedder import embed_brain
from virus.chat import start_chat

if __name__ == "__main__":
    # Check if the PDF file exists
    if not os.path.exists("virus_memory") or not os.listdir("virus_memory"):
        embed_brain("resources/brain.pdf")

    # Start the chat interface
    start_chat()