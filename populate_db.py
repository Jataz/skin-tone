import pymysql
from itertools import product
import random

# --- Skincare & Makeup Attributes ---
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

MAKEUP_SUBCATEGORIES = ["Foundation", "Concealer", "Lipstick", "Mascara", "Blush"]
FINISHES = ["Matte", "Dewy", "Satin", "Glossy"]
SHADES = ["Ivory", "Beige", "Tan", "Mocha", "Espresso"]
UNDERTONES = ["Cool", "Warm", "Neutral"]

# --- Original Skincare Recommendation Function ---
def generate_recommendation(skin_type, skin_concern):
    recommendations = []

    # By skin type
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

    # By skin concern
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
    if skin_concern in ["Sunburn"]:
        recommendations.append("After-sun care with cooling agents and SPF.")

    return " ".join(recommendations) if recommendations else "General skin-safe formulation for daily skincare."

# --- Makeup-specific Recommendation Function ---
def generate_makeup_recommendation(skin_tone, skin_type, skin_concern, undertone, subcategory):
    tips = []

    if subcategory in ["Foundation", "Concealer"]:
        tips.append("Match undertone and skin tone for best results.")
    if undertone == "Cool":
        tips.append("Use pink- or blue-based shades.")
    if undertone == "Warm":
        tips.append("Choose golden or yellow-based shades.")
    if undertone == "Neutral":
        tips.append("Neutral tones suit most skin tones.")
    if skin_type == "Oily":
        tips.append("Use matte formulas.")
    if skin_type == "Dry":
        tips.append("Dewy finishes are ideal.")

    return " ".join(tips) if tips else "Choose shades that enhance your features."

# --- Main Insert Script ---
try:
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="cosmetics_db",
        port=3306
    )
    cursor = connection.cursor()
    print("✅ Connected to database.")

    # --- Clear existing data (optional) ---
    cursor.execute("TRUNCATE TABLE products")
    print("🧹 Cleared existing products.")

    # --- Skincare Products Insert ---
    print("🔄 Inserting skincare products...")
    skincare_count = 0
    
    # Insert ALL skincare combinations
    for skin_tone, skin_type, skin_concern in product(
        SKIN_TONE_LABELS, SKIN_TYPE_LABELS, SKIN_CONCERN_LABELS
    ):
        product_name = f"{skin_concern} Treatment for {skin_tone} Skin"
        category = "Skincare"
        subcategory = None
        undertone = None
        shade = None
        finish = None
        skin_texture = random.choice(SKIN_TEXTURE_LABELS)
        link = f"http://localhost:3232/view_product?name={product_name.replace(' ', '_').lower()}"
        
        # Use the original recommendation function for skincare products
        recommendation = generate_recommendation(skin_type, skin_concern)
        makeup_recommendation = None

        query = """
        INSERT INTO products (
            name, category, subcategory, skin_tone, skin_type, skin_concern, skin_texture,
            undertone, shade, finish, link, recommendation, makeup_recommendation
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query, (
            product_name, category, subcategory, skin_tone, skin_type, skin_concern, skin_texture,
            undertone, shade, finish, link, recommendation, makeup_recommendation
        ))
        skincare_count += 1
        
        # Print progress every 50 items
        if skincare_count % 50 == 0:
            print(f"  Progress: {skincare_count} skincare products inserted...")

    print(f"✅ {skincare_count} skincare products inserted.")

    # --- Makeup Products Insert ---
    print("🔄 Inserting makeup products...")
    makeup_count = 0
    
    # Calculate how many makeup products we need to match the total
    target_makeup_count = 1125
    
    # Insert makeup combinations with a focus on creating exactly 1125 products
    for subcategory, finish, undertone, skin_tone, skin_type, skin_concern in product(
        MAKEUP_SUBCATEGORIES, FINISHES, UNDERTONES, SKIN_TONE_LABELS, SKIN_TYPE_LABELS, 
        random.sample(SKIN_CONCERN_LABELS, 5)  # Use a subset of concerns to control the total count
    ):
        # Select appropriate shade based on skin tone
        if skin_tone == "Fair":
            shade = random.choice(["Ivory", "Porcelain", "Light Beige"])
        elif skin_tone == "Medium":
            shade = random.choice(["Beige", "Tan", "Honey"])
        else:  # Dark
            shade = random.choice(["Mocha", "Espresso", "Deep"])
            
        product_name = f"{subcategory} - {shade} - {finish}"
        category = "Makeup"
        skin_texture = random.choice(SKIN_TEXTURE_LABELS)
        link = f"http://localhost:3232/view_product?name={product_name.replace(' ', '_').lower()}"
        
        # Generate makeup-specific recommendation
        makeup_recommendation = generate_makeup_recommendation(skin_tone, skin_type, skin_concern, undertone, subcategory)
        
        # For makeup products, use a generic skincare recommendation based on skin type and concern
        # This ensures the recommendation column is never NULL while keeping it different from makeup_recommendation
        recommendation = f"For {skin_type.lower()} skin with {skin_concern.lower()}, consider skincare that complements your makeup routine."
        
        query = """
        INSERT INTO products (
            name, category, subcategory, skin_tone, skin_type, skin_concern, skin_texture,
            undertone, shade, finish, link, recommendation, makeup_recommendation
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query, (
            product_name, category, subcategory, skin_tone, skin_type, skin_concern, skin_texture,
            undertone, shade, finish, link, recommendation, makeup_recommendation
        ))
        makeup_count += 1
        
        # Print progress every 50 items
        if makeup_count % 50 == 0:
            print(f"  Progress: {makeup_count} makeup products inserted...")
            
        # Stop once we reach the target count
        if makeup_count >= target_makeup_count:
            break

    connection.commit()
    print(f"✅ {makeup_count} makeup products inserted.")
    print(f"🎉 Total: {skincare_count + makeup_count} products inserted successfully.")

except pymysql.MySQLError as e:
    print(f"❌ MySQL Error: {e}")
    if connection:
        connection.rollback()
        print("⚠️ Changes rolled back due to error.")

finally:
    if connection:
        cursor.close()
        connection.close()
        print("🔒 Database connection closed.")
