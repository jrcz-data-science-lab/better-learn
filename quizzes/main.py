import subprocess

from quiz_tests import (true_false, multiple_single, multiple_answers, fill_in_the_blank, short_answer, matching)

def run_script(script_name):
    subprocess.run(["python", script_name])

def main():
    questiontype = "tf"  # we can change this to test different types

    mapping = {
        "tf": true_false,
        "mcsa": multiple_answers,
        "mcma": multiple_single,
        "fb": fill_in_the_blank,
        "sa": short_answer,
        "m": matching,
    }

    if questiontype == "all":
        for key, func in mapping.items():
            print(f"\n--- Running {key} ---")
            func()
    else:
        func = mapping.get(questiontype)
        if func:
            func()
        else:
            print(f"Unknown question type: {questiontype}")

if __name__ == "__main__":
    main()
