# LLM Prompt Sender

This Python project sends a prompt to a local LLM API, receives the response, and attempts to parse it as JSON. It’s useful for testing LLM responses and validating whether they can return properly structured JSON.

## Project Setup and Running Instructions

- **Connect WIFI with your employee accout and check the LLM via Postman**:
  - ![Postman](/send-prompt/img/postman-result.png)

- **Navigate to the project folder**:
  - Open a terminal and go to the `send-prompt` folder:
    `cd send-prompt`

- **Create a virtual environment**: You only need to create the virtual environment once
  - macOS / Linux: `python -m venv .venv`
  - Windows (cmd): `py -3 -m venv .venv`
  - Windows (PowerShell): `py -3 -m venv .venv`

- **Activate the virtual environment**: Every time you start a new terminal session to work on this project, you need to reactivate the virtual environment
  - macOS / Linux: `source .venv/bin/activate`
  - Windows (cmd): `.venv\Scripts\activate`
  - Windows (PowerShell): `.venv\Scripts\Activate.ps1`

- **Upgrade pip** (optional):
  - `python -m pip install --upgrade pip`

- **Install required libraries**:
  - `pip install -r requirements.txt` or `pip install requests`

- **Run the script**:
  - `python main.py`

## How the Main Script Works

### Imports

```python
import subprocess  
```

- `subprocess` is used to run other Python scripts from within this script.  

### Function: run_script

```python
def run_script(script_name):  
    subprocess.run(["python", script_name])  
```

- Runs a Python script specified by `script_name`.  
- Uses a list `["python", script_name]` to invoke the interpreter.  

### Main Function

```python
def main():  
    questiontype = "tf"  # we can change this later  

    mapping = {  
        "tf": "TrueFalse.py",  
        # "mcsa": "MultipleChoiceSingleAnswer.py",  
        # ... add other types here  
    }  

    script = mapping.get(questiontype)  
    if script:  
        run_script(script)  
    else:  
        print(f"Unknown question type: {questiontype}")  
```

- `questiontype` defines the type of question to generate. You can change it to other question types like 'mcsa' to run different scripts.
- `mapping` is a dictionary linking question types to their script filenames.  
- Looks up the script for the selected `questiontype`.  
- If found, calls `run_script()` to execute it.  
- If not found, prints a warning about unknown type.  

### Script Entry Point

```python
if __name__ == "__main__":  
    main()  
```

- Ensures that the script runs only when executed directly.  
- Prevents automatic execution if imported as a module in another script. 

## How the Question Generator Script Works (`TrueFalse.py` Explaination)

### Imports

```python
import requests  
import json  
```

- `requests` is used to send HTTP requests to the LLM API.  
- `json` is used to encode the request body and decode the response.  

### API URL

```python
URL = "http://145.19.54.111:11434/api/generate"
```

- Defines the endpoint where the LLM server listens.  
- The script will always send requests to this address.  

### Function Definition

```python
def test_llm():
```

- Defines a function `test_llm` that handles sending the prompt, receiving the response, and parsing it.  

### Prompt Definition

```python
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
```

- Multi-line string describing the task for the LLM.  
- Instructs the LLM to return **exactly JSON** with specific keys.  
- Provides example text for question generation.  

### Request Payload

```python
data = {  
    "model": "gemma3:27b",  
    "prompt": prompt,  
    "format": "json",  
    "stream": False  
}
```

- `model`: specifies which LLM to query. `qwen3:30b` is also recommended.
- `prompt`: the instructions to the LLM.  
- `format`: expects the output to be JSON.  
- `stream`: False → waits until the full response is ready before returning.  

**Important Parameters Info:**

| Parameter           | Type / Example     | Purpose                      | Notes                                                                 |
|---------------------|--------------------|------------------------------|----------------------------------------------------------------------|
| model               | string "gemma3:27b" <br> or "qwen3:30b" | Specify the model            | Default is gemma3:27b, can also use qwen3:30b                        |
| prompt              | string             | Task description + input text| Example: "Generate 10 multiple-choice questions as JSON"              |
| format              | string "json"      | Output format                | Forces the model to return JSON for easy parsing                      |
| stream              | boolean false      | Response mode                | false = return full result at once                                    |
| options.temperature | float 0.2          | Controls randomness          | Lower (0–0.3) recommended for more stable results                     |
| options.num_predict | integer 1000       | Max number of tokens         | Prevents overly long output or truncation                             |

### Sending the Request

```python
r = requests.post(URL, headers={"Content-Type": "application/json"}, data=json.dumps(data), timeout=30)  
r.raise_for_status()  
resp = r.json()  
text = resp.get("response", "")  
```

- Sends a POST request to the LLM API.  
- `headers`: ensures server treats body as JSON.  
- `json.dumps(data)`: converts Python dict into JSON string.  
- `timeout=30`: avoids hanging indefinitely.  
- `r.raise_for_status()`: throws error if server returns HTTP error.  
- `resp = r.json()`: parse server response into Python dict.  
- `resp.get("response", "")`: extract the actual text field.  

### Handling Empty Responses

```python
if not text:  
    print("No response content received from the LLM. Full raw response object for debugging:")  
    print(resp)  
    return  
```

- If `response` is missing or empty, print full server reply for debugging.  
- Prevents script from crashing on unexpected outputs.  

### Parsing the JSON Response

```python
try:  
    parsed = json.loads(text)  
    print("Great! Parsed JSON successfully:")  
    print(json.dumps(parsed, indent=2, ensure_ascii=False))  
except json.JSONDecodeError:  
    print("Oh no, we could not parse JSON. The raw text:")  
    print(text)  
```

- Attempts to load `text` as JSON.  
- If successful, pretty-prints parsed JSON with indentation.  
- If parsing fails, prints the raw response text for troubleshooting.  

### Error Handling

```python
except requests.exceptions.Timeout:  
    print("The model may need to be reloaded.")  
except Exception as e:  
    print("Request failed:", e)  
```

- Catches timeout errors separately, giving a specific message.  
- Any other errors are caught and printed.  

### Script Entry Point

```python
if __name__ == "__main__":  
    test_llm()  
```

- Ensures the function runs only when script is executed directly.  
- Prevents accidental execution when imported as a module.  

## Results

**True / False**:
![True or False](/send-prompt/img/tf.png)
<br>

**Multiple Choice Single Answer**:
![Multiple Choice Single Answer](/send-prompt/img/mcsa.png)
<br>

**Multiple Choice Multiple Answers**:
![Multiple Choice Multiple Answers](/send-prompt/img/mcma.png)
<br>

**Matching**:
![Matching](/send-prompt/img/m.png)
<br>

**Fill In The Blank**:
![Fill In The Blank](/send-prompt/img/fb.png)
<br>

**Short Answer**:
![Short Answer](/send-prompt/img/sa.png)