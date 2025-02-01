import pymysql

# Global database connection
connection = None

def init_db_connection():
    """Initialize and keep database connection open."""
    global connection
    if not connection:
        try:
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="",  # Default XAMPP password
                database="cosmetics_db",
                port=3306
            )
            print("DEBUG: Database connection established successfully.")
        except pymysql.MySQLError as e:
            print(f"DEBUG: Error connecting to the database: {e}")
            connection = None

def recommend_products(skin_tone, skin_type, skin_concern, skin_texture):  # FIXED ORDER
    """Recommend products based on multiple skin attributes."""
    try:
        if connection is None:
            init_db_connection()

        cursor = connection.cursor()

        # Debugging: Print received parameters
        print(f"DEBUG: Searching for products with - Tone: {skin_tone}, Type: {skin_type}, Concern: {skin_concern}, Texture: {skin_texture}")

        # Updated SQL query to allow partial matches with correct order
        query = """
        SELECT name, category,image_path, link FROM products
        WHERE LOWER(skin_tone) LIKE LOWER(%s)
        AND LOWER(skin_type) LIKE LOWER(%s)
        AND LOWER(skin_concern) LIKE LOWER(%s)
        AND LOWER(skin_texture) LIKE LOWER(%s);
        """

        # Debug: Print SQL query correctly formatted
        sql_query = query % (f"'{skin_tone}'", f"'{skin_type}'", f"'{skin_concern}'", f"'{skin_texture}'")
        print(f"DEBUG: Running SQL Query -> {sql_query}")

        cursor.execute(query, (f"%{skin_tone}%", f"%{skin_type}%", f"%{skin_concern}%", f"%{skin_texture}%"))
        products = cursor.fetchall()

        # Debugging: Print SQL results
        print(f"DEBUG: Query results: {products}")

        cursor.close()
        return products

    except pymysql.MySQLError as e:
        print(f"DEBUG: Database error: {e}")
        return []

def fetch_product_details(product_name):
    """Fetch details of a specific product by name."""
    try:
        if connection is None:
            init_db_connection()

        cursor = connection.cursor()

        # SQL query to fetch product details
        query = """
        SELECT name, category, image_path, link 
        FROM products 
        WHERE name = %s
        LIMIT 1;
        """
        cursor.execute(query, (product_name,))
        product = cursor.fetchone()

        cursor.close()
        return product

    except pymysql.MySQLError as e:
        print(f"DEBUG: Database error: {e}")
        return None
   
def fetch_gallery_products(limit=20):
    """Fetch product details including images for the gallery."""
    try:
        if connection is None:
            init_db_connection()

        cursor = connection.cursor()

        # SQL query to fetch product name, category, image path, and link
        query = """
        SELECT name, category, image_path, link FROM products 
        WHERE image_path IS NOT NULL 
        LIMIT %s;
        """
        cursor.execute(query, (limit,))
        products = cursor.fetchall()

        # Debugging: Print fetched product count
        print(f"DEBUG: Gallery Products Fetched: {len(products)} items")

        cursor.close()
        return products

    except pymysql.MySQLError as e:
        print(f"DEBUG: Database error: {e}")
        return []


def close_db_connection():
    """Close database connection on app exit."""
    global connection
    if connection:
        connection.close()
        print("DEBUG: Database connection closed successfully.")
