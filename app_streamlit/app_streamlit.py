import streamlit as st
from datetime import date
from db_connection import fetch_all, execute_query

st.title("Medical Management System")
st.sidebar.header("Menu")

# Menú de visualización
view_menu = st.sidebar.selectbox(
    "Select an option:",
    ["Doctors", "Patients", "Appointments", "Patient Prescriptions"]
)

# Menú de adición
add_menu = st.sidebar.selectbox(
    "Add New:",
    ["Add Doctor", "Add Patient", "Add Medication", "Create Prescription", "Create Appointment"]
)

def show_doctors():
    st.subheader("Doctors")
    try:
        doctors = fetch_all("SELECT * FROM doctors")
        if not doctors:
            st.write("No doctors found.")
        else:
            for doctor in doctors:
                st.write(f"{doctor['first_name']} {doctor['last_name']} - Specialization: {doctor['specialization']}")
    except Exception as e:
        st.error(f"Error fetching doctors: {e}")

def show_patients():
    st.subheader("Patients")
    patients = fetch_all("SELECT * FROM patients")
    for patient in patients:
        st.write(f"{patient['first_name']} {patient['last_name']} - Email: {patient['email']}")

def show_appointments():
    st.subheader("Appointments")
    appointments = fetch_all("SELECT a.*, d.first_name AS doctor_first_name, d.last_name AS doctor_last_name, p.first_name AS patient_first_name, p.last_name AS patient_last_name FROM appointments a JOIN doctors d ON a.doctor_id = d.id JOIN patients p ON a.patient_id = p.patient_id")
    for appointment in appointments:
        date_str = appointment['appointment_date'].strftime('%d %b %Y')
        time_str = (appointment['appointment_time'] or "00:00:00").strftime('%I:%M %p')
        st.write(f"{date_str} at {time_str} - Doctor: {appointment['doctor_first_name']} {appointment['doctor_last_name']} - Patient: {appointment['patient_first_name']} {appointment['patient_last_name']}")

def show_prescriptions():
    st.subheader("Prescriptions")
    patient_id = st.number_input("Patient ID", min_value=1, step=1)
    if st.button("Get Prescriptions"):
        prescriptions = fetch_all("SELECT * FROM prescriptions WHERE patient_id = %s", (patient_id,))
        for prescription in prescriptions:
            st.write(f"Date: {prescription['prescription_date']} - Doctor: {prescription['doctor_first_name']} {prescription['doctor_last_name']} - Notes: {prescription['notes']}")

def add_doctor():
    st.subheader("Add Doctor")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    specialization = st.text_input("Specialization")
    phone = st.text_input("Phone")
    address = st.text_area("Address")
    email = st.text_input("Email")
    
    if st.button("Save Doctor"):
        execute_query(
            "INSERT INTO doctors (first_name, last_name, specialization, phone, address, email) VALUES (%s, %s, %s, %s, %s, %s)",
            (first_name, last_name, specialization, phone, address, email)
        )
        st.success("Doctor added successfully.")

def add_patient():
    st.subheader("Add Patient")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    birth_date = st.date_input("Birth Date", value=date(2024, 1, 1))
    phone = st.text_input("Phone")
    address = st.text_area("Address")
    email = st.text_input("Email")
    
    if st.button("Save Patient"):
        execute_query(
            "INSERT INTO patients (first_name, last_name, birth_date, phone, address, email) VALUES (%s, %s, %s, %s, %s, %s)",
            (first_name, last_name, birth_date, phone, address, email)
        )
        st.success("Patient added successfully.")

def add_medication():
    st.subheader("Add Medication")
    name = st.text_input("Medication Name")
    description = st.text_area("Description")
    
    if st.button("Save Medication"):
        execute_query("INSERT INTO medications (name, description) VALUES (%s, %s)", (name, description))
        st.success("Medication added successfully.")

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
        execute_query(
            "INSERT INTO prescriptions (patient_id, doctor_id, prescription_date, notes, medication_id) VALUES (%s, %s, %s, %s, %s)",
            (selected_patient_id, selected_doctor_id, prescription_date, notes, selected_medication_id)
        )
        st.success("Prescription created successfully.")

def create_appointment():
    st.subheader("Create Appointment")
    patients = fetch_all("SELECT patient_id, CONCAT(first_name, ' ', last_name) AS name FROM patients")
    doctors = fetch_all("SELECT id, CONCAT(first_name, ' ', last_name) AS name FROM doctors")
    
    selected_patient_id = st.selectbox("Select Patient", patients, format_func=lambda x: x['name'])['patient_id']
    selected_doctor_id = st.selectbox("Select Doctor", doctors, format_func=lambda x: x['name'])['id']
    
    appointment_date = st.date_input("Appointment Date")
    appointment_time = st.time_input("Appointment Time")
    consultation_type = st.text_input("Consultation Type")
    
    if st.button("Create Appointment"):
        execute_query(
            "INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, consultation_type) VALUES (%s, %s, %s, %s, %s)",
            (selected_patient_id, selected_doctor_id, appointment_date, appointment_time, consultation_type)
        )
        st.success("Appointment created successfully!")

# Cargar vistas de acuerdo al menú
if view_menu == "Doctors":
    show_doctors()
elif view_menu == "Patients":
    show_patients()
elif view_menu == "Appointments":
    show_appointments()
elif view_menu == "Patient Prescriptions":
    show_prescriptions()

# Cargar opciones para añadir
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
