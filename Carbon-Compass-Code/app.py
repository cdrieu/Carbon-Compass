from flask import Flask, render_template, request
from calculations import calculate_total
from recommendations import generate_recommendations

app = Flask(__name__)

EMISSION_UNIT_LABEL = "tonnes CO₂e/year"
EMISSION_UNIT_NOTE = "CO₂e means carbon dioxide equivalent. 1 tonne = 1,000 kilograms."

COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Argentina",
    "Australia", "Austria", "Belgium", "Brazil", "Canada", "Chile", "China",
    "Colombia", "Denmark", "Egypt", "Finland", "France", "Germany", "Greece",
    "India", "Indonesia", "Ireland", "Israel", "Italy", "Japan", "Mexico",
    "Morocco", "Netherlands", "New Zealand", "Norway", "Pakistan", "Poland",
    "Portugal", "Singapore", "South Africa", "South Korea", "Spain", "Sweden",
    "Switzerland", "Turkey", "United Arab Emirates", "United Kingdom",
    "United States", "Vietnam", "Other"
]


def get_footprint_rating(total_tonnes):
    if total_tonnes < 4:
        return "Excellent"
    elif total_tonnes < 7:
        return "Good"
    elif total_tonnes < 10:
        return "Moderate"
    elif total_tonnes < 15:
        return "High"
    return "Very high"


def get_ranked_categories(results):
    return sorted(results["percentages"].items(), key=lambda item: item[1], reverse=True)


def coerce_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def build_answers(form):
    vehicle_types = form.getlist("vehicle_types")

    if not vehicle_types or "None" in vehicle_types:
        vehicle_types = ["None"]

    distance_unit = form.get("distance_unit", "Kilometers")
    diet = form.get("diet", "Omnivore")

    if "None" in vehicle_types:
        weekly_vehicle_distance = 0
        carpool = "Not applicable"
    else:
        weekly_vehicle_distance = coerce_float(
            form.get("weekly_vehicle_distance"),
            0
        )
        carpool = form.get("carpool", "Never")

    return {
        "country": form.get("country", ""),
        "state": form.get("state", ""),

        "household_size": coerce_float(
            form.get("household_size"),
            1
        ),

        "home_type": form.get(
            "home_type",
            "Apartment"
        ),

        "home_size": form.get(
            "home_size",
            "Medium"
        ),

        "home_systems": (
            form.getlist("home_systems")
            or ["Electricity"]
        ),

        "vehicle_types": vehicle_types,

        "weekly_vehicle_distance": weekly_vehicle_distance,

        "vehicle_distance_unit": distance_unit,

        "carpool": carpool,

        "commute": form.get(
            "commute",
            "Work from home"
        ),

        "commute_length": coerce_float(
            form.get("commute_length"),
            0
        ),

        "commute_unit": distance_unit,

        "commute_frequency": coerce_float(
            form.get("commute_frequency"),
            0
        ),

        "domestic_flights": coerce_float(
            form.get("domestic_flights"),
            0
        ),

        "international_flights": coerce_float(
            form.get("international_flights"),
            0
        ),

        "diet": diet,

        "beef_lamb_frequency": (
            form.get(
                "beef_lamb_frequency",
                "Weekly"
            )
            if diet in {
                "Omnivore",
                "Heavy meat-eater"
            }
            else "Not applicable"
        ),

        "dairy_frequency": form.get(
            "dairy_frequency",
            "Weekly"
        ),

        "food_waste": form.get(
            "food_waste",
            "Some"
        ),

        "recycles": (
            form.get("recycles", "no") == "yes"
        ),

        "composts": (
            form.get("composts", "no") == "yes"
        ),

        "trash_bags_per_week": coerce_float(
            form.get("trash_bags_per_week"),
            0
        ),

        "streaming_hours_per_day": coerce_float(
            form.get("streaming_hours_per_day"),
            0
        ),

        "ai_usage": form.get(
            "ai_usage",
            "Never"
        ),

        "video_call_hours_per_week": coerce_float(
            form.get("video_call_hours_per_week"),
            0
        ),

        "new_clothing_frequency": form.get(
            "new_clothing_frequency",
            "Sometimes"
        ),

        "new_electronics_frequency": form.get(
            "new_electronics_frequency",
            "Sometimes"
        ),
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        answers = build_answers(request.form)
        results = calculate_total(answers)
        recommendations = generate_recommendations(answers, results)
        total_tonnes = round(results["total"] / 1000, 2)

        return render_template(
            "results.html",
            results=results,
            recommendations=recommendations,
            ranked_categories=get_ranked_categories(results),
            total_tonnes=total_tonnes,
            rating=get_footprint_rating(total_tonnes),
            unit_label=EMISSION_UNIT_LABEL,
            unit_note=EMISSION_UNIT_NOTE,
        )

    return render_template("quiz.html", countries=COUNTRIES)


if __name__ == "__main__":
    app.run(debug=True)