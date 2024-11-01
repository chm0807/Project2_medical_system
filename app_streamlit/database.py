import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def fetch_all(query, params=()):
    """Fetch all records from a SELECT query."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return results

def execute_query(query, params=()):
    """Execute an INSERT, UPDATE, or DELETE query."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()
