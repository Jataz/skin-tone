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

# Database connection
try:
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="cosmetics_db",
        port=3306
    )
    cursor = connection.cursor()
    print("DEBUG: Database connection established successfully.")

    # Generate all possible combinations
    for skin_tone, skin_type, skin_concern, skin_texture in product(SKIN_TONE_LABELS, SKIN_TYPE_LABELS, SKIN_CONCERN_LABELS, SKIN_TEXTURE_LABELS):
        product_name = f"{skin_concern} Treatment for {skin_tone} Skin"
        category = "Skincare"
        link = f"http://localhost:3232/view_product?name={product_name.replace(' ', '_').lower()}"

        # SQL Insert Query
        query = """
        INSERT INTO products (name, category, skin_tone, skin_texture, skin_concern, skin_type, link)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query, (product_name, category, skin_tone, skin_texture, skin_concern, skin_type, link))

    # Commit changes
    connection.commit()
    print("DEBUG: All product combinations inserted successfully.")

except pymysql.MySQLError as e:
    print(f"ERROR: Database error: {e}")

finally:
    if connection:
        cursor.close()
        connection.close()
        print("DEBUG: Database connection closed.")
