import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Creates and returns a connection to the database."""
    try:
        print("Estableciendo conexión a la base de datos...")
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Cambia esto si tienes una contraseña
            database=" medical_appointments_service",
            port=3308
        )
        
        if connection.is_connected():
            print("Conectado a la base de datos")
            return connection
        else:
            print("Fallo al conectar a la base de datos.")
            return None
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    
def get_all_the_doctors():
    connection = get_db_connection()
    if connection is None:
        print("Fallo al establecer la conexión a la base de datos.")
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        print("Ejecutando la consulta para obtener todos los doctores...")
        cursor.execute("SELECT id, first_name, last_name, specialization, phone, address, email FROM doctors")
        doctors = cursor.fetchall()
        
        print("Consulta ejecutada. Recuperando resultados...")
        if not doctors:
            print("No se encontraron doctores en la base de datos.")
        return doctors
    except Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def main():
    print("Recuperando todos los doctores de la base de datos...")
    doctors = get_all_the_doctors()
    
    if doctors:
        print("Doctores recuperados con éxito:")
        for doctor in doctors:
            print(doctor)  # Imprimir la información de cada doctor
    else:
        print("No se encontraron doctores o ocurrió un error.")

if __name__ == "__main__":
    main()
