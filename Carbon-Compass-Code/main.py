#Carbon Compass

from questions import collect_user_answers
from calculations import calculate_total
from recommendations import generate_recommendations


def print_results(results, recommendations):
    print("\nYour Carbon Compass Results")
    print("---------------------------")
    print("Housing: " + str(results["housing"]) + " kg CO2e/year")
    print("Transportation: " + str(results["transportation"]) + " kg CO2e/year")
    print("Food: " + str(results["food"]) + " kg CO2e/year")
    print("Waste: " + str(results["waste"]) + " kg CO2e/year")
    print("Digital: " + str(results["digital"]) + " kg CO2e/year")
    print("Shopping: " + str(results["shopping"]) + " kg CO2e/year")
    print("\nTotal: " + str(results["total"]) + " kg CO2e/year")
    print("\nRecommendations")
    print("----------------")

    for recommendation in recommendations:
        print("- " + recommendation)


def main():
    answers = collect_user_answers()
    results = calculate_total(answers)
    recommendations = generate_recommendations(answers, results)
    print_results(results, recommendations)


if __name__ == "__main__":
    main()
