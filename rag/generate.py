import requests


OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "qwen2.5-coder:7b"


def generate_answer(context, question):

    prompt = f"""
You are NotesVault AI.

PRIMARY RULE:
Always prioritize the provided context/notes.

RULES:
1. First try to answer using ONLY the provided context.
2. If the answer exists in the notes, answer strictly from the notes.
3. If the answer is partially missing or completely unavailable in the notes:
   - You MAY use your own general knowledge.
   - BUT you MUST clearly mention:
     "This answer is generated using general AI knowledge and may not be from the notes."
4. NEVER falsely claim generated information came from the notes.
5. NEVER recommend external resources like YouTube, Coursera, websites, etc.
6. Keep answers concise, academic, and clear.
7. Use conversation history when needed.

Context:
{context}

Conversation:
{question}

Answer:
"""

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False, #Give full response at once, not token-by-token

                "options": {
                    "num_gpu": 0,
                    "num_ctx": 2048,
                    "temperature": 0.2
                }
            },
            timeout=180
        )

        result = response.json()

        return result.get(
            "response",
            "No response from Ollama"
        )

    except Exception as e:

        print(str(e))

        return str(e)