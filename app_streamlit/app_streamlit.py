import streamlit as st
import os
from datetime import date
from database import execute_query, fetch_all
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Interfaz de usuario
st.title("Medical Management System")
st.sidebar.header("Menu")
view_menu = st.sidebar.selectbox("Select an option:", ["Doctors", "Patients", "Appointments", "Patient Prescriptions"])
add_menu = st.sidebar.selectbox("Add New:", ["Add Doctor", "Add Patient", "Add Medication", "Create Prescription", "Create Appointment"])

# Función para mostrar doctores
@st.cache_data
def fetch_doctors():
    return fetch_all("SELECT * FROM doctors")

def show_doctors():
    st.subheader("Doctors")
    try:
        with st.spinner("Loading doctors..."):
            doctors = fetch_doctors()
            if not doctors:
                st.write("No doctors found.")
            else:
                for doctor in doctors:
                    st.write(f"{doctor['first_name']} {doctor['last_name']} - Specialization: {doctor['specialization']}")
    except Exception as e:
        st.error(f"Error fetching doctors: {e}")

# Función para mostrar pacientes
@st.cache_data
def fetch_patients():
    return fetch_all("SELECT * FROM patients")

def show_patients():
    st.subheader("Patients")
    try:
        with st.spinner("Loading patients..."):
            patients = fetch_patients()
            if not patients:
                st.write("No patients found.")
            else:
                for patient in patients:
                    st.write(f"{patient['first_name']} {patient['last_name']} - Email: {patient['email']}")
    except Exception as e:
        st.error(f"Error fetching patients: {e}")

# Función para mostrar citas
@st.cache_data
def fetch_appointments():
    return fetch_all(
        """
        SELECT a.*, d.first_name AS doctor_first_name, d.last_name AS doctor_last_name, 
                p.first_name AS patient_first_name, p.last_name AS patient_last_name 
        FROM appointments a 
        JOIN doctors d ON a.doctor_id = d.id 
        JOIN patients p ON a.patient_id = p.patient_id
        """
    )

def show_appointments():
    st.subheader("Appointments")
    try:
        with st.spinner("Loading appointments..."):
            appointments = fetch_appointments()
            if not appointments:
                st.write("No appointments found.")
            else:
                for appointment in appointments:
                    date_str = appointment['appointment_date'].strftime('%d %b %Y')
                    time_str = appointment['appointment_time'].strftime('%I:%M %p')
                    st.write(f"{date_str} at {time_str} - Doctor: {appointment['doctor_first_name']} {appointment['doctor_last_name']} - Patient: {appointment['patient_first_name']} {appointment['patient_last_name']}")
    except Exception as e:
        st.error(f"Error fetching appointments: {e}")

# Función para mostrar prescripciones
@st.cache_data
def fetch_prescriptions(patient_id):
    return fetch_all(
        """
        SELECT p.*, d.first_name AS doctor_first_name, d.last_name AS doctor_last_name 
        FROM prescriptions p 
        JOIN doctors d ON p.doctor_id = d.id 
        WHERE p.patient_id = %s
        """, (patient_id,)
    )

def show_prescriptions():
    st.subheader("Prescriptions")
    patient_id = st.number_input("Patient ID", min_value=1, step=1)
    if st.button("Get Prescriptions"):
        try:
            with st.spinner("Loading prescriptions..."):
                prescriptions = fetch_prescriptions(patient_id)
                if not prescriptions:
                    st.write("No prescriptions found for this patient.")
                else:
                    for prescription in prescriptions:
                        st.write(f"Date: {prescription['prescription_date']} - Doctor: {prescription['doctor_first_name']} {prescription['doctor_last_name']} - Notes: {prescription['notes']}")
        except Exception as e:
            st.error(f"Error fetching prescriptions: {e}")

# Función para añadir doctor
def add_doctor():
    st.subheader("Add Doctor")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    specialization = st.text_input("Specialization")
    phone = st.text_input("Phone")
    address = st.text_area("Address")
    email = st.text_input("Email")
    
    if st.button("Save Doctor"):
        if not first_name or not last_name or not specialization or not email:
            st.error("Please fill in all required fields.")
            return
        try:
            execute_query(
                "INSERT INTO doctors (first_name, last_name, specialization, phone, address, email) VALUES (%s, %s, %s, %s, %s, %s)",
                (first_name, last_name, specialization, phone, address, email)
            )
            st.success("Doctor added successfully.")
        except Exception as e:
            st.error(f"Error saving doctor: {e}")

# Función para añadir paciente
def add_patient():
    st.subheader("Add Patient")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    birth_date = st.date_input("Birth Date", value=date(2024, 1, 1))
    phone = st.text_input("Phone")
    address = st.text_area("Address")
    email = st.text_input("Email")
    
    if st.button("Save Patient"):
        if not first_name or not last_name or not email:
            st.error("Please fill in all required fields.")
            return
        try:
            execute_query(
                "INSERT INTO patients (first_name, last_name, birth_date, phone, address, email) VALUES (%s, %s, %s, %s, %s, %s)",
                (first_name, last_name, birth_date, phone, address, email)
            )
            st.success("Patient added successfully.")
        except Exception as e:
            st.error(f"Error saving patient: {e}")

# Función para añadir medicación
def add_medication():
    st.subheader("Add Medication")
    name = st.text_input("Medication Name")
    description = st.text_area("Description")
    
    if st.button("Save Medication"):
        if not name:
            st.error("Please fill in the medication name.")
            return
        try:
            execute_query("INSERT INTO medications (name, description) VALUES (%s, %s)", (name, description))
            st.success("Medication added successfully.")
        except Exception as e:
            st.error(f"Error saving medication: {e}")

# Función para crear prescripción
def create_prescription():
    st.subheader("Create Prescription")
    patients = fetch_all("SELECT patient_id, CONCAT(first_name, ' ', last_name) AS name FROM patients")
    doctors = fetch_all("SELECT id, CONCAT(first_name, ' ', last_name) AS name FROM doctors")
    medications = fetch_all("SELECT medication_id, name FROM medications")
    
    selected_patient_id = st.selectbox("Select Patient", patients, format_func=lambda x: x['name'])['patient_id']
    selected_doctor_id = st.selectbox("Select Doctor", doctors, format_func=lambda x: x['name'])['id']
    selected_medication_id = st.selectbox("Select Medication", medications, format_func=lambda x: x['name'])['medication_id']
    
    prescription_date = st.date_input("Prescription Date")
    notes = st.text_area("Notes")
    
    if st.button("Save Prescription"):
        if not notes:
            st.error("Please enter notes for the prescription.")
            return
        try:
            execute_query(
                "INSERT INTO prescriptions (patient_id, doctor_id, prescription_date, notes, medication_id) VALUES (%s, %s, %s, %s, %s)",
                (selected_patient_id, selected_doctor_id, prescription_date, notes, selected_medication_id)
            )
            st.success("Prescription created successfully.")
        except Exception as e:
            st.error(f"Error saving prescription: {e}")

# Función para crear cita
def create_appointment():
    st.subheader("Create Appointment")
    patients = fetch_all("SELECT patient_id, CONCAT(first_name, ' ', last_name) AS name FROM patients")
    doctors = fetch_all("SELECT id, CONCAT(first_name, ' ', last_name) AS name FROM doctors")

    selected_patient_id = st.selectbox("Select Patient", patients, format_func=lambda x: x['name'])['patient_id']
    selected_doctor_id = st.selectbox("Select Doctor", doctors, format_func=lambda x: x['name'])['id']
    appointment_date = st.date_input("Appointment Date")
    appointment_time = st.time_input("Appointment Time")

    if st.button("Save Appointment"):
        try:
            execute_query(
                "INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time) VALUES (%s, %s, %s, %s)",
                (selected_patient_id, selected_doctor_id, appointment_date, appointment_time)
            )
            st.success("Appointment created successfully.")
        except Exception as e:
            st.error(f"Error saving appointment: {e}")

# Mostrar información según las selecciones
if view_menu == "Doctors":
    show_doctors()
elif view_menu == "Patients":
    show_patients()
elif view_menu == "Appointments":
    show_appointments()
elif view_menu == "Patient Prescriptions":
    show_prescriptions()

if add_menu == "Add Doctor":
    add_doctor()
elif add_menu == "Add Patient":
    add_patient()
elif add_menu == "Add Medication":
    add_medication()
elif add_menu == "Create Prescription":
    create_prescription()
elif add_menu == "Create Appointment":
    create_appointment()


