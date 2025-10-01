import requests
import json

URL = "http://145.19.54.111:11434/api/generate"

def test_llm():
    prompt = """
    Create 2 Multiple Choice (Multiple Answers) questions based on the text below.
    Return only a JSON array. Each object must have:
    - id: number
    - type: "mcma"
    - question: string
    - options: ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5", "Option 6"]
    - answer: ["Option X", "Option Y"]  # list of correct options (2 correct answers)

    Text: Python is a programming language.
    """

    data = {
        "model": "gemma3:27b",
        "prompt": prompt,
        "format": "json",
        "stream": False
    }

    try:
        r = requests.post(URL, headers={"Content-Type": "application/json"}, data=json.dumps(data), timeout=60)
        r.raise_for_status()
        resp = r.json()
        text = resp.get("response", "")

        if not text:
            print("No response content received from the LLM. Full raw response object for debugging:")
            print(resp)
            return

        try:
            parsed = json.loads(text)
            print("Great! Parsed JSON successfully:")
            print(json.dumps(parsed, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("Oh no, we could not parse JSON. The raw text:")
            print(text)

    except requests.exceptions.Timeout:
        print("The model may need to be reloaded.")
    except Exception as e:
        print("Request failed:", e)


if __name__ == "__main__":
    test_llm()
