# Backend(FastAPI + Uvicorn)

## How to start the server
### 1. Activate the virtual environment
macOS / Linux:<br>
`source .venv/bin/activate`

Windows (cmd)：<br>
`.venv\Scripts\activate`

Windows (PowerShell)：<br>
`.venv\Scripts\Activate.ps1`

### 2. Start the server
`uvicorn main:app --reload --port 8000`

### 3. Optional: Only use one command to activate and start the server
macOS / Linux:<br>
`source .venv/bin/activate && uvicorn main:app --reload --port 8000`

Windows (PowerShell):<br>
`.venv\Scripts\Activate.ps1; uvicorn main:app --reload --port 8000`

### 4. Optional: Install the dependencies
`pip install -r ./requirements.txt`

### 5. Run the API
`python ./main.py`