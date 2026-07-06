#Carbon Compass: Emission Factor Storage

HOUSEHOLD_ALLOCATION_FACTOR = "divide_by_household_size"

HOME_TYPE_ENERGY_MMBTU = {
    "Apartment": 54.4,
    "Townhouse": 89.3,
    "Detached house": 108.4,
    "Dormitory": None,
    "Other": 89.3
}

DORM_EMISSIONS_KG_PER_STUDENT_YEAR = 1641

HOME_SIZE_FACTORS = {
    "Small": 0.43,
    "Medium": 1.00,
    "Large": 1.67,
    "Very large": 2.33
}

HOUSING_FACTORS = {
    "electricity_kg_co2e_per_kwh": 0.350,
    "heating_kg_co2_per_cubic_foot_natural_gas": 0.055,
    "air_conditioning_kg_co2e_per_kwh": 0.350
}

VEHICLE_FACTORS_KG_PER_MILE = {
    "Gasoline car": 0.400,
    "Hybrid vehicle": 0.303,
    "Electric car": 0.101,
    "Motorcycle": 0.182
}

VEHICLE_FACTORS_KG_PER_KM = {
    "Gasoline car": 0.249,
    "Hybrid vehicle": 0.188,
    "Electric car": 0.063,
    "Motorcycle": 0.113
}

COMMUTE_FACTORS_KG_PER_KM = {
    "Car": 0.170,
    "Bus": 0.097,
    "Train": 0.035,
    "Bicycle": 0.033,
    "Walk": 0.000,
    "Work from home": 0.000,
    "Other": 0.097
}

FLIGHT_FACTORS_KG_PER_PASSENGER_KM = {
    "Domestic": 0.246,
    "International": 0.150,
    "Short haul": 0.244,
    "Medium haul": 0.153,
    "Long haul": 0.150
}

# NOTE: These used to be full annual diet baselines, which already assumed
# an average amount of beef/lamb/dairy consumption for each diet type. That
# meant beef/lamb and dairy were being counted once here AND again from the
# frequency questions below, double-counting a big chunk of the food
# footprint. These are now baselines for everything EXCEPT beef, lamb, and
# dairy (grains, produce, pork, poultry, seafood, eggs, plant protein,
# processed foods). Beef/lamb and dairy are always added on top from the
# user's actual reported frequency, for every diet type.
DIET_BASE_KG_PER_YEAR_EXCL_BEEF_LAMB_DAIRY = {
    "Vegan": 504,
    "Vegetarian": 550,
    "Pescetarian": 700,
    "Omnivore": 900,
    "Heavy meat-eater": 1300
}

# Kept for reference/back-compat; no longer used directly in calculations.py
DIET_FACTORS_KG_PER_YEAR = {
    "Vegan": 504,
    "Vegetarian": 894,
    "Pescetarian": 993,
    "Omnivore": 1617,
    "Heavy meat-eater": 2624
}

FOOD_FACTORS = {
    "beef_kg_co2e_per_kg": 99,
    "beef_kg_co2e_per_125g_serving": 12.38,
    "lamb_kg_co2e_per_kg": 40,
    "lamb_kg_co2e_per_100g_serving": 4.00,
    "dairy_kg_co2e_per_kg": 3.15,
    "pork_kg_co2e_per_kg": 12.3,
    "poultry_kg_co2e_per_kg": 9.9,
    "seafood_kg_co2e_per_kg": 13.6,
    "eggs_kg_co2e_per_kg": 4.7,
    "plant_protein_kg_co2e_per_kg": 2.0,
    "food_waste_kg_co2e_per_kg": 1.90
}

FREQUENCY_TO_SERVINGS_PER_WEEK = {
    "Not applicable": 0,
    "Never": 0,
    "Rarely": 1,
    "Weekly": 2,
    "Several times per week": 5,
    "Daily": 7
}

FOOD_WASTE_LEVEL_KG_PER_WEEK = {
    "None": 0,
    "A little": 1,
    "Some": 3,
    "A lot": 6
}

WASTE_FACTORS = {
    "landfill_kg_co2e_per_kg": 0.573,
    "recycling_kg_co2e_avoided_per_month": 61,
    "composting_kg_co2e_per_kg": 0.022,
    "assumed_trash_bag_kg": 7
}

DIGITAL_FACTORS = {
    "video_music_streaming_kg_co2e_per_hour": 0.055,
    "music_streaming_kg_co2e_per_hour": 0.001,
    "ai_kg_co2e_per_query": 0.0022,
    "video_calling_kg_co2e_per_hour": 0.016
}

AI_FREQUENCY_TO_QUERIES_PER_WEEK = {
    "Never": 0,
    "Rarely": 3,
    "Weekly": 10,
    "Daily": 35
}

SHOPPING_FACTORS = {
    "new_clothing_kg_co2e_per_garment": 18.39,
    "fast_fashion_multiplier": 1.50,
    "second_hand_avoidance_factor": 0.80,
    "electronics_kg_co2e_per_device": 62,
    "furniture_home_goods_kg_co2e_per_item": 139.5,
    "repair_reuse_avoidance_factor": 0.50
}

SHOPPING_FREQUENCY_TO_ITEMS_PER_YEAR = {
    "Rarely": 2,
    "Sometimes": 6,
    "Often": 12,
    "Frequently": 24
}