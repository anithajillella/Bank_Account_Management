from database import get_connection

try:
    connection = get_connection()

    if connection.is_connected():
        print("Database connected successfully!")

except Exception as e:
    print("Database connection failed:", e)

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed.")