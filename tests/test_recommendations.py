import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Carbon-Compass-Code")))

from recommendations import generate_recommendations


def test_generate_recommendations_returns_top_three_ranked_categories():
    answers = {"recycles": False, "composts": False}
    results = {
        "housing": 1000,
        "transportation": 2000,
        "food": 1500,
        "waste": 500,
        "digital": 100,
        "shopping": 300,
        "total": 5400,
        "percentages": {
            "housing": 18.5,
            "transportation": 37.0,
            "food": 27.8,
            "waste": 9.3,
            "digital": 1.9,
            "shopping": 5.6,
        },
    }

    recommendations = generate_recommendations(answers, results)

    assert len(recommendations) == 3
    assert [item["category"] for item in recommendations] == ["transportation", "food", "housing"]
    assert recommendations[0]["percent_of_footprint"] == 37.0
    assert recommendations[0]["kg_saved"] is not None
    assert recommendations[0]["percent_saved"] is not None


def test_generate_recommendations_includes_waste_only_when_relevant():
    answers = {"recycles": True, "composts": True}
    results = {
        "housing": 1000,
        "transportation": 1000,
        "food": 1000,
        "waste": 1000,
        "digital": 100,
        "shopping": 100,
        "total": 5200,
        "percentages": {
            "housing": 19.2,
            "transportation": 19.2,
            "food": 19.2,
            "waste": 19.2,
            "digital": 1.9,
            "shopping": 1.9,
        },
    }

    recommendations = generate_recommendations(answers, results)

    assert all(item["category"] != "waste" for item in recommendations)
