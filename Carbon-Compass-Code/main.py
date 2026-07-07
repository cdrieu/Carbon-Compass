#Carbon Compass: Collects user answers, calculates footprint, generates recommendations, & prints results.

from questions import collect_user_answers
from calculations import calculate_total
from recommendations import generate_recommendations

EMISSION_UNIT_LABEL = "tonnes CO₂e/year"
EMISSION_UNIT_NOTE = "All emissions are shown in tonnes CO₂e (1 tonne = 1000 kilograms)."


def get_ranked_categories(results):
    return sorted(results["percentages"].items(), key=lambda item: item[1], reverse=True)


def get_footprint_rating(total_tonnes):
    if total_tonnes < 4:
        return "Excellent"
    elif total_tonnes < 7:
        return "Good"
    elif total_tonnes < 10:
        return "Moderate"
    elif total_tonnes < 15:
        return "High"
    else:
        return "Very high"


def print_results(results):
    total_tonnes = round(results["total"] / 1000, 2)
    rating = get_footprint_rating(total_tonnes)

    print("\nYour Carbon Compass Results")
    print("---------------------------")
    print(EMISSION_UNIT_NOTE)
    print("Housing: " + str(round(results["housing"] / 1000, 2)) + " " + EMISSION_UNIT_LABEL)
    print("Transportation: " + str(round(results["transportation"] / 1000, 2)) + " " + EMISSION_UNIT_LABEL)
    print("Food: " + str(round(results["food"] / 1000, 2)) + " " + EMISSION_UNIT_LABEL)
    print("Waste: " + str(round(results["waste"] / 1000, 2)) + " " + EMISSION_UNIT_LABEL)
    print("Digital: " + str(round(results["digital"] / 1000, 2)) + " " + EMISSION_UNIT_LABEL)
    print("Shopping: " + str(round(results["shopping"] / 1000, 2)) + " " + EMISSION_UNIT_LABEL)

    print("\nTotal: " + str(total_tonnes) + " " + EMISSION_UNIT_LABEL)
    print("Footprint rating: " + rating)


def print_rankings(results):
    print("\nBiggest Contributors")
    print("--------------------")

    for category, percent in get_ranked_categories(results):
        print(category.capitalize() + ": " + str(round(percent)) + "%")


def print_recommendations(recommendations):
    print("\nRecommendations")
    print("----------------")

    total_saved_percent = 0

    for i, rec in enumerate(recommendations, start=1):
        print(f"\n{i}. {rec['category'].title()} — {rec['percent_of_footprint']}% of your footprint")
        print(rec["message"])

        if rec["kg_saved"] is not None:
            total_saved_percent += rec["percent_saved"]
            print(
                f"Potential savings: ~{round(rec['kg_saved'] / 1000, 2)} {EMISSION_UNIT_LABEL} "
                f"({rec['percent_saved']}% off your total footprint)"
            )

    if total_saved_percent > 0:
        print(
            "\nTogether, these recommendations could reduce your footprint by approximately "
            + str(round(total_saved_percent, 1))
            + "% if consistently adopted."
        )


def main():
    answers = collect_user_answers()
    results = calculate_total(answers)
    recommendations = generate_recommendations(answers, results)

    print_results(results)
    print_rankings(results)
    print_recommendations(recommendations)


if __name__ == "__main__":
    main()