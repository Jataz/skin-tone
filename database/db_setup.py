import mysql.connector

def setup_database():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cosmetics_db"
    )
    cursor = connection.cursor()

    # Create products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        category VARCHAR(255),
        skin_tone VARCHAR(255),
        texture VARCHAR(255),
        condition VARCHAR(255),
        link TEXT
    )
    """)
    connection.commit()
    cursor.close()
    connection.close()

def insert_sample_data():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="cosmetics_db"
    )
    cursor = connection.cursor()
    
    # Insert sample products
    sample_data = [
        ("Foundation A", "Foundation", "Fair", "Smooth", "Dry", "http://example.com/foundation-a"),
        ("Foundation B", "Foundation", "Medium", "Rough", "Oily", "http://example.com/foundation-b"),
        ("Lipstick X", "Lipstick", "Dark", "Smooth", "Oily", "http://example.com/lipstick-x"),
    ]
    cursor.executemany("""
    INSERT INTO products (name, category, skin_tone, texture, condition, link)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, sample_data)
    connection.commit()
    cursor.close()
    connection.close()
