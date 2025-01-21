import pymysql

try:
    # Establish connection using PyMySQL
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",  # Default XAMPP password is empty
        database="cosmetics_db",
        port=3306
    )
    if connection:
        print("Connected to MySQL database using PyMySQL!")

    # Query the database
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products;")
    rows = cursor.fetchall()
    if rows:
        print("Data retrieved:")
        for row in rows:
            print(row)
    else:
        print("No data found in the 'products' table.")

    # Close connection
    cursor.close()
    connection.close()

except pymysql.MySQLError as err:
    print(f"MySQL error: {err}")
except Exception as e:
    print(f"Unexpected error: {e}")
