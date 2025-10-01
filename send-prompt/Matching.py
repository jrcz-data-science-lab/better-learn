import requests
import json

URL = "http://145.19.54.111:11434/api/generate"

def test_llm():
    prompt = """
    Create 1 Matching question based on the text below.
    Return only a JSON object with:
    - id: number
    - type: "m"
    - question: string
    - left_options: ["A1", "A2", "A3"]
    - right_options: ["B1", "B2", "B3"]
    - answer: {"A1":"B2", "A2":"B3", "A3":"B1"}  # correct pairs

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
