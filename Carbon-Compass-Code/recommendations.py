# Carbon Compass: Personalized Recommendations

def generate_recommendations(answers, results):

    recommendations = []

    percentages = results["percentages"]

    categories = sorted(
        percentages.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for category, percent in categories[:3]:

        if category == "transportation":
            recommendations.append(
                f"Transportation represents {percent}% of your footprint, and it's also probably your biggest hidden expense. Carpooling or public transit can save you real money on gas and parking, cycling for short trips doubles as free cardio, and cutting a few unnecessary drives a week gives you back time you'd otherwise spend behind the wheel."
            )

        elif category == "food":
            recommendations.append(
                f"Food represents {percent}% of your footprint. Cutting back on beef and lamb is one of the highest-leverage changes you can make for your footprint, and it tends to come with lower grocery bills and a lighter, less inflammatory diet as a side effect. You don't necessarily have to go all-in, even swapping two or three meals a week can add up."
            )

        elif category == "housing":
            recommendations.append(
                f"Housing contributes {percent}% of your footprint. Your home energy use is a major lever here, and it's one that pays you back directly: better insulation, smarter thermostat habits, or just a few degrees of adjustment on heating and cooling can meaningfully shrink your utility bills while cutting emissions."
            )

        elif category == "shopping":
            recommendations.append(
                f"Shopping represents {percent}% of your footprint. Buying fewer new clothes and electronics, or choosing second-hand, cuts emissions substantially and tends to save serious money too. It's also a good nudge toward a less cluttered, more intentional relationship with what you own."
            )

        elif category == "digital":
            recommendations.append(
                f"Digital activities account for {percent}% of your footprint. Trimming excess streaming or AI usage barely dents your day-to-day experience, but it's a quiet way to reclaim a little screen time and lower your energy use at the same time."
            )

        elif category == "waste":
            recommendation = (
                f"Waste contributes {percent}% of your footprint. Continuing to reduce landfill waste through recycling and composting can make an additional difference. "
            )

            if not answers["recycles"]:
                recommendation += "Recycling more of your household materials is a low-effort habit that keeps waste out of landfills, and it's one of the easiest ways to feel like your daily choices are actually adding up to something. "

            if not answers["composts"]:
                recommendation += "Composting food scraps prevents methane emissions from landfills, and if you garden or keep houseplants, it also hands you free, nutrient-rich soil instead of paying for it at the store."

            recommendations.append(recommendation.strip())

    return recommendations