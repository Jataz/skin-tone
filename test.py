import pymysql
from itertools import product
import os
from PIL import Image, ImageDraw, ImageFont

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

# Ensure the static/images directory exists
IMAGE_DIR = "static/images"
os.makedirs(IMAGE_DIR, exist_ok=True)

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
        image_filename = f"{product_name.replace(' ', '_').lower()}.png"
        image_path = os.path.join(IMAGE_DIR, image_filename).replace("\\", "/")  # Normalize path
        link = f"http://localhost:3232/view_product?name={product_name.replace(' ', '_').lower()}"

        # Generate and save the image
        img = Image.new("RGB", (400, 300), color=(255, 235, 205))  # Light beige background
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 18)  # Try system font
        except:
            font = ImageFont.load_default()  # Use default if arial is not available

        # Draw text on image
        draw.text((20, 50), f"{skin_concern} Treatment", font=font, fill=(50, 50, 50))
        draw.text((20, 100), f"Tone: {skin_tone}", font=font, fill=(80, 80, 80))
        draw.text((20, 150), f"Type: {skin_type}", font=font, fill=(80, 80, 80))
        draw.text((20, 200), f"Texture: {skin_texture}", font=font, fill=(80, 80, 80))

        # Save image
        img.save(image_path)
        print(f"DEBUG: Image saved -> {image_path}")

        # SQL Insert Query
        query = """
        INSERT INTO products (name, category, skin_tone, skin_texture, skin_concern, skin_type, link, image_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query, (product_name, category, skin_tone, skin_texture, skin_concern, skin_type, link, image_path))

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
