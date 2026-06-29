#Carbon Compass
from questions import collect_user_answers


def print_answers(answers):
    """Print a clean summary of the user's answers."""
    print("\nYour Carbon Compass Answers")
    print("---------------------------")

    for key, value in answers.items():
        print(key + ": " + str(value))


def main():
    answers = collect_user_answers()
    print_answers(answers)


main()