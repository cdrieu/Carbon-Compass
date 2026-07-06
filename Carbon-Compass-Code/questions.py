#Carbon Compass: Question Bank

def ask_number(question):
    """Ask the user for a number and return it as a float."""
    return float(input(question + " "))


def ask_choice(question, choices):
    """Ask the user to choose one option from a numbered list."""
    print("\n" + question)

    for i, choice in enumerate(choices, start=1):
        print(str(i) + ". " + choice)

    answer = int(input("Enter a number: "))
    return choices[answer - 1]


def ask_multi_choice(question, choices):
    """Ask the user to choose multiple options from a numbered list."""
    print("\n" + question)
    print("Enter all that apply, separated by commas.")

    for i, choice in enumerate(choices, start=1):
        print(str(i) + ". " + choice)

    raw_answer = input("Enter numbers: ")
    selected = []

    for number in raw_answer.split(","):
        number = number.strip()

        if number != "":
            index = int(number) - 1
            selected.append(choices[index])

    return selected


def ask_slider_choice(question, choices):
    """Ask the user to choose from an ordered slider-like scale."""
    return ask_choice(question, choices)


def ask_yes_no(question):
    """Ask a yes/no question."""
    answer = input(question + " (yes/no) ").lower()

    while answer != "yes" and answer != "no":
        answer = input("Please enter yes or no: ").lower()

    return answer == "yes"


def collect_user_answers():
    """Collect all quiz answers from the user."""
    answers = {}

    print("Welcome to Carbon Compass!")
    print("Let's estimate your carbon footprint.\n")

    answers["country"] = input("What country do you live in? ")
    answers["state"] = input("What state/province do you live in? ")

    answers["household_size"] = ask_number("How many people live in your household?")

    answers["home_type"] = ask_choice(
        "What type of home do you live in?",
        ["Apartment", "Townhouse", "Detached house", "Dormitory", "Other"]
    )

    answers["home_size"] = ask_slider_choice(
        "Approximately how large is your home?",
        ["Small", "Medium", "Large", "Very large"]
    )

    answers["home_systems"] = ask_multi_choice(
        "Which of these does your home use?",
        ["Electricity", "Heating", "Air conditioning"]
    )

    answers["vehicle_types"] = ask_multi_choice(
        "Which motor vehicles do you regularly use?",
        ["Gasoline car", "Hybrid vehicle", "Electric car", "Motorcycle", "None"]
    )

    if "None" not in answers["vehicle_types"]:
        answers["weekly_vehicle_distance"] = ask_number(
            "Approximately how many kilometers/miles do you drive each week?"
        )

        answers["carpool"] = ask_slider_choice(
            "How often do you carpool?",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        )
    else:
        answers["weekly_vehicle_distance"] = 0
        answers["carpool"] = "Not applicable"

    answers["commute"] = ask_choice(
        "How do you usually commute?",
        ["Car", "Bus", "Train", "Bicycle", "Walk", "Work from home", "Other"]
    )

    answers["commute_length"] = ask_number(
        "How far is your one-way commute?"
    )

    answers["commute_frequency"] = ask_number(
        "How many days per week do you commute?"
    )

    answers["domestic_flights"] = ask_number(
        "How many domestic flights do you take each year on average?"
    )

    answers["international_flights"] = ask_number(
        "How many international flights do you take each year on average?"
    )

    answers["diet"] = ask_choice(
        "Which best describes your diet?",
        ["Vegan", "Vegetarian", "Pescetarian", "Omnivore", "Heavy meat-eater"]
    )

    if answers["diet"] == "Omnivore" or answers["diet"] == "Heavy meat-eater":
        answers["beef_lamb_frequency"] = ask_slider_choice(
            "How often do you eat beef or lamb?",
            ["Never", "Rarely", "Weekly", "Several times per week", "Daily"]
        )
    else:
        answers["beef_lamb_frequency"] = "Not applicable"

    answers["dairy_frequency"] = ask_slider_choice(
        "How often do you consume dairy?",
        ["Never", "Rarely", "Weekly", "Several times per week", "Daily"]
    )

    answers["food_waste"] = ask_slider_choice(
        "How much food do you typically throw away?",
        ["None", "A little", "Some", "A lot"]
    )

    answers["recycles"] = ask_yes_no("Do you recycle?")

    answers["composts"] = ask_yes_no("Do you compost?")

    answers["trash_bags_per_week"] = ask_number(
        "How many trash bags does your household fill per week?"
    )

    answers["streaming_hours_per_day"] = ask_number(
        "How many hours per day do you stream video or music?"
    )

    answers["ai_usage"] = ask_slider_choice(
        "How often do you use AI tools?",
        ["Never", "Rarely", "Weekly", "Daily"]
    )

    answers["video_call_hours_per_week"] = ask_number(
        "How many hours do you spend on video calls each week?"
    )

    answers["new_clothing_frequency"] = ask_slider_choice(
        "How often do you buy new clothing?",
        ["Rarely", "Sometimes", "Often", "Frequently"]
    )

    answers["new_electronics_frequency"] = ask_slider_choice(
        "How often do you buy new electronics?",
        ["Rarely", "Sometimes", "Often", "Frequently"]
    )

    return answers