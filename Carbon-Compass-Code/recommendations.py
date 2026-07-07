#Carbon Compass: Personalized Recommendations

TRANSPORTATION_REDUCTION_FACTOR = 0.15
FOOD_REDUCTION_FACTOR = 0.12
HOUSING_REDUCTION_FACTOR = 0.10
SHOPPING_REDUCTION_FACTOR = 0.20
DIGITAL_REDUCTION_FACTOR = 0.10
WASTE_RECYCLE_REDUCTION_FACTOR = 0.25
WASTE_COMPOST_REDUCTION_FACTOR = 0.20


CATEGORY_MESSAGES = {
    "transportation": (
        "Transportation represents {percent}% of your footprint, and it is also one of the biggest hidden costs in everyday life. "
        "Driving less, carpooling, using public transit, or cycling for shorter trips can cut fuel use while saving money. "
        "Choosing trains when possible and combining trips can make a meaningful difference too."
    ),
    "food": (
        "Food represents {percent}% of your footprint. Cutting back on beef, lamb, and dairy is one of the highest-leverage changes you can make. "
        "You do not have to go all-in: swapping a few meals a week, choosing more plant-based proteins, or reducing dairy where it feels realistic can have a strong impact."
    ),
    "housing": (
        "Housing contributes {percent}% of your footprint. Your home energy use is a major lever here, and it is one that pays you back directly: better insulation, "
        "smarter thermostat habits, or a few degrees of adjustment on heating and cooling can significantly shrink your utility bills while cutting emissions."
    ),
    "shopping": (
        "Shopping represents {percent}% of your footprint. Buying fewer new clothes and electronics, or choosing second-hand, cuts emissions substantially and tends to save money too."
    ),
    "digital": (
        "Digital activities account for {percent}% of your footprint. Trimming excess streaming or AI usage is a simple way to lower energy use."
    ),
}


def _calculate_percent_saved(results, kg_saved):
    if results["total"] <= 0:
        return 0.0
    return round((kg_saved / results["total"]) * 100, 1)


def _rank_categories(results):
    return sorted(results["percentages"].items(), key=lambda item: item[1], reverse=True)


def _build_waste_message(answers, percent):
    message = (
        f"Waste contributes {percent}% of your footprint. Continuing to reduce landfill waste through recycling and composting can make an additional difference. "
    )

    if not answers.get("recycles", True):
        message += "Recycling more household materials is a low-effort habit that keeps waste out of landfills. "

    if not answers.get("composts", True):
        message += "Composting food scraps prevents methane emissions from landfills."

    return message.strip()


def _estimate_savings(category, answers, results):
    if category == "transportation":
        kg_saved = results["transportation"] * TRANSPORTATION_REDUCTION_FACTOR
    elif category == "food":
        kg_saved = results["food"] * FOOD_REDUCTION_FACTOR
    elif category == "housing":
        kg_saved = results["housing"] * HOUSING_REDUCTION_FACTOR
    elif category == "shopping":
        kg_saved = results["shopping"] * SHOPPING_REDUCTION_FACTOR
    elif category == "digital":
        kg_saved = results["digital"] * DIGITAL_REDUCTION_FACTOR
    elif category == "waste":
        kg_saved = 0.0
        if not answers.get("recycles", True):
            kg_saved += results["waste"] * WASTE_RECYCLE_REDUCTION_FACTOR
        if not answers.get("composts", True):
            kg_saved += results["waste"] * WASTE_COMPOST_REDUCTION_FACTOR
    else:
        return None

    if kg_saved <= 0:
        return None

    return round(kg_saved, 2), _calculate_percent_saved(results, kg_saved)


def generate_recommendations(answers, results, top_n=3):
    recommendations = []

    for category, percent in _rank_categories(results):
        if len(recommendations) >= top_n:
            break

        if category == "waste":
            if answers.get("recycles", True) and answers.get("composts", True):
                continue
            message = _build_waste_message(answers, percent)
        elif category in CATEGORY_MESSAGES:
            message = CATEGORY_MESSAGES[category].format(percent=percent)
        else:
            continue

        savings = _estimate_savings(category, answers, results)

        recommendations.append({
            "category": category,
            "percent_of_footprint": percent,
            "message": message,
            "kg_saved": savings[0] if savings else None,
            "percent_saved": savings[1] if savings else None,
        })

    return recommendations