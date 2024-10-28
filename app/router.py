from fastapi import APIRouter, HTTPException
from models import DoctorCreate, PatientCreate, AppointmentCreate, PrescriptionCreate, MedicationCreate
from db_connection import get_db_connection
from typing import List
import mysql.connector

router = APIRouter()

# Listar doctores
@router.get("/doctors/", response_model=List[DoctorCreate])
def list_doctors():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM doctors")
        doctors = cursor.fetchall()
        return doctors
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# Crear un nuevo doctor
@router.post("/doctors/", response_model=DoctorCreate)
def create_doctor(doctor: DoctorCreate):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        INSERT INTO doctors (first_name, last_name, specialization, phone, address, email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (doctor.first_name, doctor.last_name, doctor.specialization, doctor.phone, doctor.address, doctor.email)
        
        cursor.execute(query, values)
        conn.commit()
        
        new_doctor_id = cursor.lastrowid
        doctor.id = new_doctor_id
        return doctor

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# Listar pacientes
@router.get("/patients/", response_model=List[PatientCreate])
def list_patients():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchall()
        return patients
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# Crear un nuevo paciente
@router.post("/patients/", response_model=PatientCreate)
def create_patient(patient: PatientCreate):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        INSERT INTO patients (first_name, last_name, birth_date, phone, address, email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (patient.first_name, patient.last_name, patient.birth_date, patient.phone, patient.address, patient.email)
        
        cursor.execute(query, values)
        conn.commit()
        
        new_patient_id = cursor.lastrowid
        patient.patient_id = new_patient_id
        return patient

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# Listar citas
@router.get("/appointments/", response_model=List[AppointmentCreate])
def list_appointments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM appointments")
        appointments = cursor.fetchall()
        return appointments
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# Crear una nueva cita
@router.post("/appointments/", response_model=AppointmentCreate)
def create_appointment(appointment: AppointmentCreate):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, consultation_type)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (appointment.patient_id, appointment.doctor_id, appointment.appointment_date, appointment.appointment_time, appointment.consultation_type)
        
        cursor.execute(query, values)
        conn.commit()
        
        new_appointment_id = cursor.lastrowid
        appointment.appointment_id = new_appointment_id
        return appointment

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# Listar medicamentos
@router.get("/medications/", response_model=List[MedicationCreate])
def list_medications():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM medications")
        medications = cursor.fetchall()
        return medications
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# Crear un nuevo medicamento
@router.post("/medications/", response_model=MedicationCreate)
def create_medication(medication: MedicationCreate):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        INSERT INTO medications (name, description)
        VALUES (%s, %s)
        """
        values = (medication.name, medication.description)
        
        cursor.execute(query, values)
        conn.commit()
        
        new_medication_id = cursor.lastrowid
        medication.medication_id = new_medication_id
        return medication

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# Crear una nueva receta
@router.post("/prescriptions/", response_model=PrescriptionCreate)
def create_prescription(prescription: PrescriptionCreate):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        INSERT INTO prescriptions (patient_id, doctor_id, prescription_date, notes)
        VALUES (%s, %s, %s, %s)
        """
        values = (prescription.patient_id, prescription.doctor_id, prescription.prescription_date, prescription.notes)
        
        cursor.execute(query, values)
        conn.commit()
        
        new_prescription_id = cursor.lastrowid
        prescription.prescription_id = new_prescription_id
        return prescription

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()
