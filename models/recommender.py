import pymysql

# Create a global connection object to keep it open for multiple analyses
connection = None

def init_db_connection():
    """Initialize the database connection and keep it open."""
    global connection
    if not connection:
        try:
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="",  # Default XAMPP password is empty
                database="cosmetics_db",
                port=3306  # Default MySQL port
            )
            print("DEBUG: Database connection established successfully.")
        except pymysql.MySQLError as e:
            print(f"DEBUG: Error connecting to the database: {e}")
            connection = None

def recommend_products(skin_tone, texture, conditiontype):
    """Recommend products based on skin tone, texture, and condition type."""
    try:
        # Ensure the database connection is initialized
        if connection is None:
            init_db_connection()
        
        # Create a cursor for executing queries
        cursor = connection.cursor()

        # Debug: Print input parameters
        print(f"DEBUG: Querying products for skin_tone='{skin_tone}', texture='{texture}', conditiontype='{conditiontype}'")

        # Query products
        query = """
        SELECT name, category, link FROM products
        WHERE LOWER(skin_tone) = LOWER(%s) AND LOWER(texture) = LOWER(%s) AND LOWER(conditiontype) = LOWER(%s);
        """
        cursor.execute(query, (skin_tone, texture, conditiontype))
        products = cursor.fetchall()

        # Debug: Print query results
        print(f"DEBUG: Query results: {products}")

        cursor.close()  # Close the cursor but keep the connection open
        return products

    except pymysql.MySQLError as e:
        print(f"DEBUG: Database error: {e}")
        return []

def close_db_connection():
    """Close the database connection when the application exits."""
    global connection
    if connection:
        connection.close()
        print("DEBUG: Database connection closed successfully.")
