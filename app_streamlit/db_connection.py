import mysql.connector
from mysql.connector import Error

def get_db_connection():
    return mysql.connector.connect(
            host='localhost',  
            user='root',      
            password='',      
            database='medical_appointments_service',  
            port=3308         
        )

def fetch_all(query, params=None):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error fetching data: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def execute_query(query, params=None):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
    except Error as e:
        print(f"Error executing query: {e}")
    finally:
        cursor.close()
        connection.close()
