# PDF and PPTX Text Extraction

This Python project extracts text from both PDF and PPTX files. It ensures the extracted text keeps the correct reading order, removes empty lines, and preserves the last line completely.

## Project Setup and Running Instructions

- **Navigate to the project folder**:
  - Open a terminal and go to the `extract-text` folder:
    `cd extract-text`

- **Create a virtual environment**:
  - A virtual environment isolates project dependencies from the system Python, preventing conflicts and ensuring reproducibility (You only need to create the virtual environment once).
    - macOS / Linux: `python -m venv .venv`
    - Windows (cmd): `py -3 -m venv .venv`
    - Windows (PowerShell): `py -3 -m venv .venv`

- **Activate the virtual environment**:
  - Ensures that Python and pip use the environment's isolated packages (Every time you start a new terminal session to work on this project, you need to reactivate the virtual environment).
    - macOS / Linux: `source .venv/bin/activate`
    - Windows (cmd): `.venv\Scripts\activate`
    - Windows (PowerShell): `.venv\Scripts\Activate.ps1`

- **Upgrade pip** (optional):
  - Make sure pip is up to date: `python -m pip install --upgrade pip`

- **Install required libraries**:
  - Install all dependencies from the requirements file: `pip install -r requirements.txt`

- **Run the script**:
  - Execute the main Python script to extract PDF and PPTX text: `python main.py`
  - This command works on macOS, Linux, and Windows (cmd or PowerShell) as long as the virtual environment is activated.

## How the Script Works

### Imports
```python
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from pptx import Presentation
```

- `extract_text` is a high-level function from `pdfminer.six` used to extract text from PDF files.
- `LAParams` is the layout analysis parameters class, controlling how PDF lines, paragraphs, and columns are interpreted.
- `Presentation` from `python-pptx` opens PPTX files, allowing access to slides, shapes, and text.

### PDF Text Extraction Function
```python
def extract_pdf_text(path):
    laparams = LAParams(char_margin=1.5, line_margin=0.8, word_margin=0.1, boxes_flow=0.5)
    text = extract_text(path, laparams=laparams)
    
    if text and not text.endswith('\n'):
        text += '\n'
    
    lines = [line for line in text.splitlines() if line.strip()]
    
    if lines and not lines[-1].endswith(('.', '?', '!', '…')):
        lines[-1] += '.'
    
    return "\n".join(lines)
```

- **Define a function `extract_pdf_text`**, with parameter `path` as the PDF file path.

- **Create an `LAParams` instance** to control PDF layout analysis:
  - `char_margin=1.5`: maximum spacing between characters; if spacing is less, they are treated as the same word.
  - `line_margin=0.8`: line spacing threshold; lines closer than this are considered part of the same paragraph.
  - `word_margin=0.1`: word spacing threshold; words closer than this are merged into the same line.
  - `boxes_flow=0.5`: controls horizontal layout recognition; 0=strictly by columns, 1=strictly by text flow, 0.5=balanced.

- **Call `extract_text`** to extract text from the PDF using the specified `LAParams`.
  - Returns a string containing all text from the PDF.

- **Ensure the last line ends with a newline**:
  - Prevents losing or misjoining the final sentence.
  - `text and not text.endswith('\n')`: checks that text is not empty and does not already end with a newline.

- **Split the PDF text into lines**:
  - `splitlines()` separates text at newline characters.
  - `[line for line in ... if line.strip()]` filters out completely empty lines.
  - Result is a list `lines` containing only non-empty lines.

- **Check the last line for sentence-ending punctuation**:
  - `lines[-1].endswith(('.', '?', '!', '…'))`: determines if the last line ends properly.
  - If not, add a period to complete the final sentence.

- **Join lines into a single string**:
  - Use newline characters `\n`.
  - Returns the complete text string of the PDF.

### PPTX Text Extraction Function
```python
def extract_pptx_text(path):
    prs = Presentation(path)
    texts = []
    for slide in prs.slides:
        shapes = [s for s in slide.shapes if s.has_text_frame]
        shapes.sort(key=lambda s: (s.top, s.left))
        for shape in shapes:
            line = shape.text.strip()
            if line:
                texts.append(line)
    return "\n".join(texts)
```

- **Define `extract_pptx_text`** with parameter `path` as the PPTX file path.

- **Open the PPTX file**:
  - Returns a `Presentation` object `prs`.
  - `prs.slides` allows access to all slides in the presentation.

- **Initialize a list `texts`** to store each line of extracted text.

- **Iterate over each slide**.

- **Filter shapes with text**:
  - Each slide may contain many shapes (text boxes, images, charts, etc.).
  - Keep only shapes that have text frames (`s.has_text_frame`).

- **Sort shapes by position**:
  - `s.top`: the y-coordinate of the top edge of the shape.
  - `s.left`: the x-coordinate of the left edge of the shape.
  - Ensures reading order from top to bottom, left to right.

- **Extract text from each shape**:
  - Use `shape.text` to get full text.
  - Apply `strip()` to remove leading and trailing spaces.
  - If text is not empty, append to the `texts` list.

- **Join all text into a single string**:
  - Use newline characters `\n`.
  - Returns the complete text string of the PPTX.

### Main Execution
```python
if __name__ == "__main__":
    pdf_text = extract_pdf_text("./sample_files/sample.pdf")
    print("PDF Content:\n", pdf_text, "\n")

    pptx_text = extract_pptx_text("./sample_files/sample.pptx")
    print("PPTX Content:\n", pptx_text, "\n")
```

- **Python entry point check**:
  - `if __name__ == "__main__":` ensures that the following code only runs when the script is executed directly.
  - If the script is imported as a module in another script, this section will not run, preventing unintended execution.

- **Extract PDF text**:
  - The function `extract_pdf_text()` requires a parameter `path` which tells the function the **exact location of the PDF file** to read.
  - `pdf_text = extract_pdf_text("./sample_files/sample.pdf")` passes the relative path `"./sample_files/sample.pdf"` to the function.
  - The function reads the PDF at this location, extracts all text, and stores it in the variable `pdf_text`.
  - Printing `pdf_text` outputs the **entire content of the PDF**, without limiting the number of characters.

- **Extract PPTX text**:
  - Similarly, the function `extract_pptx_text()` requires a `path` parameter for the PPTX file location.
  - `pptx_text = extract_pptx_text("./sample_files/sample.pptx")` passes the relative path to the function.
  - The function reads this PPTX file, extracts all text from slides in reading order, and stores it in `pptx_text`.
  - Printing `pptx_text` outputs the **full content of the PPTX**, ensuring no truncation.

- **Key Point about Parameters (`path`)**:
  - `path` is not predefined; it is **supplied when calling the function**.
  - The function uses the string you pass as `path` to locate and open the correct file.
  - The function will only process the specific file you pass; it does **not automatically search the folder** or pick files based on extension.
