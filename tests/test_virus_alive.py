# test_virus_alive.py

from virus.chat import load_virus_chat

qa = load_virus_chat()

query = "What is your purpose?"
response = qa.run(query)

assert "assist" in response.lower() or "answer" in response.lower()
print("[✓] VIRUS is still operational.")
