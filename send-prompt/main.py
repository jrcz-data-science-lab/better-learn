import subprocess

def run_script(script_name):
    subprocess.run(["python", script_name])

def main():
    questiontype = "mcma"  # we can change this later

    mapping = {
        "tf": "TrueFalse.py",
        "mcsa": "MultipleChoiceSingleAnswer.py",
        "mcma": "MultipleChoiceMultipleAnswers.py",
        # ... add other types here
    }

    script = mapping.get(questiontype)
    if script:
        run_script(script)
    else:
        print(f"Unknown question type: {questiontype}")

if __name__ == "__main__":
    main()
