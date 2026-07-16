#Carbon Compass: Calculations
from data import (
    VEHICLE_FACTORS_KG_PER_KM,
    COMMUTE_FACTORS_KG_PER_KM,
    FLIGHT_FACTORS_KG_PER_PASSENGER_KM,
    DIET_BASE_KG_PER_YEAR_EXCL_BEEF_LAMB_DAIRY,
    FREQUENCY_TO_SERVINGS_PER_WEEK,
    FOOD_FACTORS,
    FOOD_WASTE_LEVEL_KG_PER_WEEK,
    WASTE_FACTORS,
    DIGITAL_FACTORS,
    AI_FREQUENCY_TO_QUERIES_PER_WEEK,
    SHOPPING_FACTORS,
    SHOPPING_FREQUENCY_TO_ITEMS_PER_YEAR,
    HOME_SIZE_FACTORS,
    HOME_TYPE_ENERGY_MMBTU,
    DORM_EMISSIONS_KG_PER_STUDENT_YEAR,
    HOUSING_FACTORS,
)


def calculate_housing(answers):

    household_size = max(answers["household_size"], 1)

    if answers["home_type"] == "Dormitory":

        return DORM_EMISSIONS_KG_PER_STUDENT_YEAR

    home_energy_mmbtu = HOME_TYPE_ENERGY_MMBTU[answers["home_type"]]

    size_factor = HOME_SIZE_FACTORS[answers["home_size"]]

    total_mmbtu = home_energy_mmbtu * size_factor

    systems = answers["home_systems"]

    electricity_emissions = 0

    heating_emissions = 0

    air_conditioning_emissions = 0

    if "Electricity" in systems:

        electricity_kwh = total_mmbtu * 293.071 * 0.50

        electricity_emissions = (

            electricity_kwh

            * HOUSING_FACTORS["electricity_kg_co2e_per_kwh"]

        )

    if "Heating" in systems:

        heating_mmbtu = total_mmbtu * 0.35

        heating_cubic_feet = heating_mmbtu * 970

        heating_emissions = (

            heating_cubic_feet

            * HOUSING_FACTORS[

                "heating_kg_co2_per_cubic_foot_natural_gas"

            ]

        )

    if "Air conditioning" in systems:

        ac_kwh = total_mmbtu * 293.071 * 0.15

        air_conditioning_emissions = (

            ac_kwh

            * HOUSING_FACTORS[

                "air_conditioning_kg_co2e_per_kwh"

            ]

        )

    grid_electricity_emissions = (

        electricity_emissions

        + air_conditioning_emissions

    )

    if "Solar panels" in systems:

        solar_reduction = min(
            HOUSING_FACTORS["solar_panel_reduction_kg_per_household_year"],
            grid_electricity_emissions,
        )
        grid_electricity_emissions -= solar_reduction
    housing_emissions = (
        grid_electricity_emissions
        + heating_emissions
    )

    return max(housing_emissions / household_size, 0)


def calculate_transportation(answers):
    total = 0

    weekly_distance = answers["weekly_vehicle_distance"]

    if answers.get("vehicle_distance_unit") == "Miles":
        weekly_distance_km = weekly_distance * 1.60934
    else:
        weekly_distance_km = weekly_distance

    if "None" not in answers["vehicle_types"]:
        for vehicle in answers["vehicle_types"]:
            if vehicle in VEHICLE_FACTORS_KG_PER_KM:
                total += weekly_distance_km * VEHICLE_FACTORS_KG_PER_KM[vehicle] * 52

    commute_mode = answers["commute"]
    commute_distance_km = answers["commute_length"]

    if answers["commute_unit"] == "Miles":
        commute_distance_km *= 1.60934

    commute_days = answers["commute_frequency"]

    if commute_mode in COMMUTE_FACTORS_KG_PER_KM:
        total += commute_distance_km * 2 * commute_days * 52 * COMMUTE_FACTORS_KG_PER_KM[commute_mode]

    total += answers["domestic_flights"] * 1000 * FLIGHT_FACTORS_KG_PER_PASSENGER_KM["Domestic"]
    total += answers["international_flights"] * 6500 * FLIGHT_FACTORS_KG_PER_PASSENGER_KM["International"]

    return total


def calculate_food(answers):
    total = DIET_BASE_KG_PER_YEAR_EXCL_BEEF_LAMB_DAIRY[answers["diet"]]

    beef_lamb_frequency = answers.get("beef_lamb_frequency", "Not applicable")
    beef_lamb_servings = FREQUENCY_TO_SERVINGS_PER_WEEK.get(beef_lamb_frequency, 0)
    total += beef_lamb_servings * FOOD_FACTORS["beef_kg_co2e_per_125g_serving"] * 52

    dairy_servings = FREQUENCY_TO_SERVINGS_PER_WEEK[answers["dairy_frequency"]]
    total += dairy_servings * 0.25 * FOOD_FACTORS["dairy_kg_co2e_per_kg"] * 52

    food_waste_kg_per_week = FOOD_WASTE_LEVEL_KG_PER_WEEK[answers["food_waste"]]
    total += food_waste_kg_per_week * FOOD_FACTORS["food_waste_kg_co2e_per_kg"] * 52

    return total


def calculate_waste(answers):
    household_size = max(answers["household_size"], 1)

    trash_kg_per_week = answers["trash_bags_per_week"] * WASTE_FACTORS["assumed_trash_bag_kg"]
    total = trash_kg_per_week * WASTE_FACTORS["landfill_kg_co2e_per_kg"] * 52
    total = total / household_size

    if answers["recycles"]:
        total *= 0.75

    if answers["composts"]:
        total *= 0.80

    return total


def calculate_digital(answers):
    total = 0

    total += answers["streaming_hours_per_day"] * DIGITAL_FACTORS["video_music_streaming_kg_co2e_per_hour"] * 365

    ai_queries_per_week = AI_FREQUENCY_TO_QUERIES_PER_WEEK[answers["ai_usage"]]
    total += ai_queries_per_week * DIGITAL_FACTORS["ai_kg_co2e_per_query"] * 52

    total += answers["video_call_hours_per_week"] * DIGITAL_FACTORS["video_calling_kg_co2e_per_hour"] * 52

    return total


def calculate_shopping(answers):
    total = 0

    clothing_items_per_year = SHOPPING_FREQUENCY_TO_ITEMS_PER_YEAR[answers["new_clothing_frequency"]]
    total += clothing_items_per_year * SHOPPING_FACTORS["new_clothing_kg_co2e_per_garment"]

    electronics_items_per_year = SHOPPING_FREQUENCY_TO_ITEMS_PER_YEAR[answers["new_electronics_frequency"]]
    total += electronics_items_per_year * SHOPPING_FACTORS["electronics_kg_co2e_per_device"]

    return total


def calculate_total(answers):
    housing = calculate_housing(answers)
    transportation = calculate_transportation(answers)
    food = calculate_food(answers)
    waste = calculate_waste(answers)
    digital = calculate_digital(answers)
    shopping = calculate_shopping(answers)

    total = (
        housing
        + transportation
        + food
        + waste
        + digital
        + shopping
    )

    percentages = {
        "housing": round(housing / total * 100, 1),
        "transportation": round(transportation / total * 100, 1),
        "food": round(food / total * 100, 1),
        "waste": round(waste / total * 100, 1),
        "digital": round(digital / total * 100, 1),
        "shopping": round(shopping / total * 100, 1),
    }

    return {
        "housing": round(housing, 2),
        "transportation": round(transportation, 2),
        "food": round(food, 2),
        "waste": round(waste, 2),
        "digital": round(digital, 2),
        "shopping": round(shopping, 2),
        "total": round(total, 2),
        "percentages": percentages,
    }