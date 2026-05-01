import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_summary(metadata):
    prompt = f"""
    You are a data analyst.

    Generate a clear dataset description based on:
    {metadata}

    Include:
    - What this dataset contains
    - Possible use cases
    - Important columns
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]