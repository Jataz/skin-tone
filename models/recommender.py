import mysql.connector

def recommend_products(skin_tone, texture, conditiontype):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cosmetics_db"
    )
    cursor = connection.cursor()

    # Fetch products matching the user's profile
    query = """
    SELECT name, category, link FROM products
    WHERE skin_tone = %s AND texture = %s AND conditiontype = %s
    """
    cursor.execute(query, (skin_tone, texture, conditiontype))
    products = cursor.fetchall()
    cursor.close()
    connection.close()

    return products
