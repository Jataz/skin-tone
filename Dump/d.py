import pymysql
from itertools import product

# Define possible values
SKIN_TONE_LABELS = ["Fair", "Medium", "Dark"]
SKIN_TYPE_LABELS = ["Normal", "Dry", "Oily", "Combination", "Sensitive"]
SKIN_CONCERN_LABELS = [
    "Cystic Acne", "Blackheads", "Whiteheads",
    "Hyperpigmentation", "Melasma", "Dark Spots",
    "Fine Lines", "Wrinkles", "Aging",
    "Dullness", "Dehydration",
    "Redness", "Rosacea", "Irritation", "Sunburn"
]
SKIN_TEXTURE_LABELS = [
    "Velvety", "Soft", "Smooth",
    "Flaky", "Harsh", "Rough",
    "Patchy", "Uneven", "Bumpy",
    "Large Pores",
    "Peeling", "Tight", "Scaly"
]

# Skincare Recommendation Generator
def generate_skincare_recommendation(skin_type, skin_concern):
    recommendations = []

    # Skin type
    if skin_type == "Oily":
        recommendations.append("Oil-free or non-comedogenic to minimize clogged pores.")
    if skin_type == "Sensitive":
        recommendations.append("Hypoallergenic to reduce the risk of irritation.")
    if skin_type in ["Oily", "Combination"]:
        recommendations.append("Lightweight formulas to avoid exacerbating oiliness.")
    if skin_type == "Dry":
        recommendations.append("Hydrating products with ingredients like hyaluronic acid.")
    if skin_type == "Normal":
        recommendations.append("Balanced products for daily maintenance.")

    # Skin concern
    if skin_concern in ["Blackheads", "Whiteheads", "Cystic Acne"]:
        recommendations.append("Buildable coverage to conceal without clogging pores.")
        recommendations.append("Ingredients like salicylic acid or benzoyl peroxide.")
    if skin_concern in ["Wrinkles", "Fine Lines", "Aging"]:
        recommendations.append("Anti-aging formulas with retinol or peptides.")
    if skin_concern in ["Hyperpigmentation", "Melasma", "Dark Spots"]:
        recommendations.append("Brightening ingredients like Vitamin C or Niacinamide.")
    if skin_concern in ["Redness", "Rosacea", "Irritation"]:
        recommendations.append("Soothing ingredients like Aloe Vera or Chamomile.")
    if skin_concern in ["Dullness", "Dehydration"]:
        recommendations.append("Revitalizing serums and moisturizers with hyaluronic acid.")
    if skin_concern == "Sunburn":
        recommendations.append("After-sun care with cooling agents and SPF.")

    return " ".join(recommendations) if recommendations else "General skin-safe formulation for daily skincare."

# Makeup Recommendation Generator
def generate_makeup_recommendation(skin_tone, skin_type, skin_concern):
    recommendations = []

    # Skin tone
    if skin_tone == "Fair":
        recommendations.append("Use neutral or pink undertones for foundation.")
    elif skin_tone == "Medium":
        recommendations.append("Choose golden or peach undertones.")
    elif skin_tone == "Dark":
        recommendations.append("Go for rich, warm undertones with deep pigments.")

    # Skin type
    if skin_type == "Oily":
        recommendations.append("Opt for matte foundations or powders.")
    elif skin_type == "Dry":
        recommendations.append("Use hydrating or dewy finish foundations.")
    elif skin_type == "Sensitive":
        recommendations.append("Choose fragrance-free and hypoallergenic products.")

    # Skin concern
    if skin_concern in ["Cystic Acne", "Blackheads", "Whiteheads"]:
        recommendations.append("Use non-comedogenic makeup and avoid heavy layers.")
    if skin_concern in ["Hyperpigmentation", "Melasma", "Dark Spots"]:
        recommendations.append("Use full-coverage concealers with color-correcting bases.")
    if skin_concern in ["Wrinkles", "Fine Lines", "Aging"]:
        recommendations.append("Avoid thick or drying products that settle in lines.")
    if skin_concern in ["Redness", "Rosacea", "Irritation"]:
        recommendations.append("Green-tinted primers or CC creams can neutralize redness.")
    if skin_concern in ["Dullness"]:
        recommendations.append("Use illuminating primers or highlighters.")

    return " ".join(recommendations) if recommendations else "Choose makeup that enhances your natural look."

# Connect to database and insert
try:
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="cosmetics_db",
        port=3306
    )
    cursor = connection.cursor()
    print("DEBUG: Database connection established.")

    # Loop over all combinations
    count = 0
    for skin_tone, skin_type, skin_concern, skin_texture in product(SKIN_TONE_LABELS, SKIN_TYPE_LABELS, SKIN_CONCERN_LABELS, SKIN_TEXTURE_LABELS):
        product_name = f"{skin_concern} Treatment for {skin_tone} Skin"
        category = "Skincare"
        link = f"http://localhost:3232/view_product?name={product_name.replace(' ', '_').lower()}"
        skincare_recommendation = generate_skincare_recommendation(skin_type, skin_concern)
        makeup_recommendation = generate_makeup_recommendation(skin_tone, skin_type, skin_concern)

        query = """
        INSERT INTO products (
            name, category, skin_tone, skin_texture, skin_concern, skin_type, link, recommendation, makeup
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query, (
            product_name, category, skin_tone, skin_texture,
            skin_concern, skin_type, link,
            skincare_recommendation, makeup_recommendation
        ))
        count += 1

    connection.commit()
    print(f"DEBUG: All {count} product combinations inserted with skincare and makeup recommendations.")

except pymysql.MySQLError as e:
    print(f"ERROR: Database error occurred - {e}")

finally:
    if connection:
        cursor.close()
        connection.close()
        print("DEBUG: Database connection closed.")
