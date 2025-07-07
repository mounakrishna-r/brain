# tests/test_virus_alive.py

from core.llm_setup import load_retrieval_chain

def test_basic_response():
    qa = load_retrieval_chain()
    query = "What is your purpose?"
    response = qa.run(query)

    assert isinstance(response, str)
    assert any(word in response.lower() for word in ["assist", "help", "answer", "support"])

    print("[✓] JARVIS assistant is responsive and coherent.")

if __name__ == "__main__":
    test_basic_response()
