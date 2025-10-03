import requests
import json

URL = "http://145.19.54.111:11434/api/generate"

def call_llm(prompt):
    data = {
        "model": "gemma3:27b",
        "prompt": prompt,
        "stream": False,
    }

    try:
        r = requests.post(URL, 
        headers={"Content-Type": "application/json"}, 
        data=json.dumps(data), 
        timeout=60)

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

def fill_in_the_blank():
    prompt = """
Create 1 Fill-in-the-Blank question based on the text below.
    Return only a JSON object with:
    - id: number
    - type: "fb"
    - question: string  # sentence with two blanks
    - answer: ["word1", "word2"]  # correct words for the blanks

    Text: Python is a programming language."""

    text = call_llm(prompt)
    print(text)

def multiple_answers():
        prompt = """
Create 2 Multiple Choice (Multiple Answers) questions based on the text below.
    Return only a JSON array. Each object must have:
    - id: number
    - type: "mcma"
    - question: string
    - options: ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5", "Option 6"]
    - answer: ["Option X", "Option Y"]  # list of correct options (2 correct answers)

    Text: Python is a programming language."""
        
        text = call_llm(prompt)
        print(text)

def true_false():
        prompt = """
 Create 2 True/False questions based on the text below.
    Return only a JSON array. Each object must have:
    - id: number
    - type: "tf"
    - question: string
    - options: ["True", "False"]
    - answer: "True" or "False"

    Text: Python is a programming language.
"""
        text = call_llm(prompt)
        print(text)

def short_answer():
        prompt = """
  Create 1 Short Answer question based on the text below.
    Return only a JSON object with:
    - id: number
    - type: "sa"
    - question: string
    - answer: string  # the correct answer

    Text: Python is a programming language. """
        
        text = call_llm(prompt)
        print(text)

def matching():
        prompt = """
Create 1 Matching question based on the text below.
    Return only a JSON object with:
    - id: number
    - type: "m"
    - question: string
    - left_options: ["A1", "A2", "A3"]
    - right_options: ["B1", "B2", "B3"]
    - answer: {"A1":"B2", "A2":"B3", "A3":"B1"}  # correct pairs

    Text: Python is a programming language."""
        text = call_llm(prompt)
        print(text)

def multiple_single():
        prompt = """
Create 2 Multiple Choice (Single Answer) questions based on the text below.
    Return only a JSON array. Each object must have:
    - id: number
    - type: "mcsa"
    - question: string
    - options: ["Option 1", "Option 2", "Option 3", "Option 4"]
    - answer: "Option 1" or "Option 2" or "Option 3" or "Option 4"

    Text: Python is a programming language."""
        text = call_llm(prompt)
        print(text)
    
if __name__ == "__main__":
  tests = {
      "tf": true_false,
        "mcsa": multiple_single,
        "mcma": multiple_answers,
        "fb": fill_in_the_blank,
        "sa": short_answer,
        "m": matching,
  }

  print("Select a test to run:")
  print("fb = Fill in the Blank")
  print("mcma = Multiple Choice Multiple Answers")      
  print("tf = True/False")
  print("sa = Short Answer")
  print("m = Matching")
  print("mcsa = Multiple Choice Single Answer")

  choice = input("Enter the number of the test to run (1-6): ")
  test_keys = list(tests.keys())  
  if choice in map(str, range(1, len(test_keys) + 1)):
      selected_test = test_keys[int(choice) - 1]
      print(f"Running test: {selected_test}")
      tests[selected_test]()
  else:
      print("Invalid choice. Please select a number between 1 and 6.")
