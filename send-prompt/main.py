import subprocess

def run_script(script_name):
    subprocess.run(["python", script_name])

def main():
    questiontype = "sa"  # we can change this to test different types

    mapping = {
        "tf": "TrueFalse.py",
        "mcsa": "MultipleChoiceSingleAnswer.py",
        "mcma": "MultipleChoiceMultipleAnswers.py",
        "fb": "FillInTheBlank.py",
        "sa": "ShortAnswer.py",
        "m": "Matching.py",
        # ... add other types here
    }

    script = mapping.get(questiontype)
    if script:
        run_script(script)
    else:
        print(f"Unknown question type: {questiontype}")

if __name__ == "__main__":
    main()
