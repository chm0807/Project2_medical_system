import streamlit as st
import requests
from datetime import datetime, timedelta, date

st.title("Medical Management System")
st.sidebar.header("Menu")

menu = st.sidebar.selectbox(
    "Select an option:",
    ["Doctors", "Patients", "Appointments", "Patient Prescriptions", "Add Doctor", "Add Patient", "Add Medication", "Create Prescription", "Prescription Medications"]
)

def show_doctors():
    st.subheader("Doctors")
    response = requests.get('http://127.0.0.1:5000/doctors')
    if response.status_code == 200:
        doctors = response.json()
        for doctor in doctors:
            st.write(f"{doctor['first_name']} {doctor['last_name']} - Specialization: {doctor['specialization']}")
    else:
        st.error("Error retrieving doctors list.")

def show_patients():
    st.subheader("Patients")
    response = requests.get('http://127.0.0.1:5000/patients')
    if response.status_code == 200:
        patients = response.json()
        for patient in patients:
            st.write(f"{patient['first_name']} {patient['last_name']} - Email: {patient['email']}")
    else:
        st.error("Error retrieving patients list.")

def show_appointments():
    st.subheader("Appointments")
    response = requests.get('http://127.0.0.1:5000/appointments')
    if response.status_code == 200:
        appointments = response.json()
        for appointment in appointments:
            appointment_date = datetime.strptime(appointment['appointment_date'], '%a, %d %b %Y %H:%M:%S %Z').strftime('%d %b %Y')
            if isinstance(appointment['appointment_time'], str):
                appointment_time = datetime.strptime(appointment['appointment_time'], '%H:%M:%S').strftime('%I:%M %p')
            elif isinstance(appointment['appointment_time'], (float, int)):
                total_seconds = int(appointment['appointment_time'])
                appointment_time = str(timedelta(seconds=total_seconds))
                appointment_time = datetime.strptime(appointment_time, '%H:%M:%S').strftime('%I:%M %p')
            else:
                appointment_time = "Unknown Time"
            st.write(f"{appointment_date} at {appointment_time} - Doctor: {appointment['doctor_first_name']} {appointment['doctor_last_name']} - Patient: {appointment['patient_first_name']} {appointment['patient_last_name']}")
    else:
        st.error(f"Error retrieving appointments list: {response.status_code} - {response.text}")

def show_prescriptions():
    st.subheader("Prescriptions")
    patient_id = st.number_input("Patient ID", min_value=1, step=1)
    if st.button("Get Prescriptions"):
        response = requests.get(f'http://127.0.0.1:5000/prescriptions/{patient_id}')
        if response.status_code == 200:
            prescriptions = response.json()
            for prescription in prescriptions:
                st.write(f"Date: {prescription['prescription_date']} - Doctor: {prescription['doctor_first_name']} {prescription['doctor_last_name']} - Notes: {prescription['notes']}")
        else:
            st.error("Error retrieving prescriptions for the specified patient.")

def add_doctor():
    st.subheader("Add Doctor")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    specialization = st.text_input("Specialization")
    phone = st.text_input("Phone")
    address = st.text_area("Address")
    email = st.text_input("Email")
    
    if st.button("Save Doctor"):
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "specialization": specialization,
            "phone": phone,
            "address": address,
            "email": email
        }
        response = requests.post('http://127.0.0.1:5000/doctors', json=data)
        if response.status_code == 201:
            st.success("Doctor added successfully.")
        else:
            st.error("Error adding doctor.")

def add_patient():
    st.subheader("Add Patient")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    min_date = date(1900, 1, 1)
    max_date = date.today()
    birth_date = st.date_input("Birth Date", value=date(2024, 1, 1), min_value=min_date, max_value=max_date)
    phone = st.text_input("Phone")
    address = st.text_area("Address")
    email = st.text_input("Email")
    
    if st.button("Save Patient"):
        birth_date_str = datetime.combine(birth_date, datetime.min.time()).strftime('%Y-%m-%d')
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date_str,
            "phone": phone,
            "address": address,
            "email": email
        }
        response = requests.post('http://127.0.0.1:5000/patients', json=data)
        if response.status_code == 201:
            st.success("Patient added successfully.")
        else:
            st.error("Error adding patient.")

def add_medication():
    st.subheader("Add Medication")
    name = st.text_input("Medication Name")
    description = st.text_area("Description")
    
    if st.button("Save Medication"):
        data = {
            "name": name,
            "description": description
        }
        response = requests.post('http://127.0.0.1:5000/medications', json=data)
        if response.status_code == 201:
            st.success("Medication added successfully.")
        else:
            st.error("Error adding medication.")

def create_prescription():
    st.subheader("Create Prescription")
    response = requests.get('http://127.0.0.1:5000/patients')
    if response.status_code == 200:
        patients = response.json()
        patient_options = [(patient['patient_id'], f"{patient['first_name']} {patient['last_name']}") for patient in patients]
        selected_patient_id = st.selectbox('Select Patient', patient_options, format_func=lambda x: x[1])
    else:
        st.error(f"Error retrieving patients: {response.status_code} - {response.text}")

    response = requests.get('http://127.0.0.1:5000/doctors')
    if response.status_code == 200:
        doctors = response.json()
        doctor_options = [(doctor['id'], f"{doctor['first_name']} {doctor['last_name']}") for doctor in doctors]
        selected_doctor_id = st.selectbox('Select Doctor', doctor_options, format_func=lambda x: x[1])
    else:
        st.error(f"Error retrieving doctors: {response.status_code} - {response.text}")

    response = requests.get('http://127.0.0.1:5000/medications')
    if response.status_code == 200:
        medications = response.json()
        medication_options = [(med['medication_id'], med['name']) for med in medications]
        selected_medication_id = st.selectbox('Select Medication', medication_options, format_func=lambda x: x[1])
    else:
        st.error(f"Error retrieving medications: {response.status_code} - {response.text}")

    prescription_date = st.date_input("Prescription Date")
    notes = st.text_area("Notes")

    if st.button("Save Prescription"):
        data = {
            "patient_id": selected_patient_id[0],
            "doctor_id": selected_doctor_id[0],
            "prescription_date": prescription_date.strftime('%Y-%m-%d'),
            "notes": notes,
            "medication_id": selected_medication_id[0]
        }
        response = requests.post('http://127.0.0.1:5000/prescriptions', json=data)
        if response.status_code == 201:
            st.success("Prescription created successfully.")
        else:
            st.error("Error creating prescription.")

def show_prescription_medications():
    st.subheader("Prescription Medications")
    prescription_id = st.number_input("Prescription ID", min_value=1, step=1)
    if st.button("Get Medications"):
        response = requests.get(f'http://127.0.0.1:5000/prescription_medications/{prescription_id}')
        if response.status_code == 200:
            medications = response.json()
            for med in medications:
                st.write(f"Medication: {med['name']} - Dosage: {med['dosage']} - Frequency: {med['frequency']}")
        else:
            st.error("Error retrieving medications for the specified prescription.")

def create_appointment():
    st.subheader('Create Appointment')
    response = requests.get('http://127.0.0.1:5000/patients')
    if response.status_code == 200:
        patients = response.json()
        patient_options = [(patient['patient_id'], f"{patient['first_name']} {patient['last_name']}") for patient in patients]
        selected_patient_id = st.selectbox('Select Patient', patient_options, format_func=lambda x: x[1])
    else:
        st.error(f"Error retrieving patients: {response.status_code} - {response.text}")

    response = requests.get('http://127.0.0.1:5000/doctors')
    if response.status_code == 200:
        doctors = response.json()
        doctor_options = [(doctor['id'], f"{doctor['first_name']} {doctor['last_name']}") for doctor in doctors]
        selected_doctor_id = st.selectbox('Select Doctor', doctor_options, format_func=lambda x: x[1])
    else:
        st.error(f"Error retrieving doctors: {response.status_code} - {response.text}")

    appointment_date = st.date_input('Appointment Date')
    appointment_time = st.time_input('Appointment Time')
    consultation_type = st.text_input('Consultation Type')

    if st.button('Create Appointment'):
        new_appointment = {
            'patient_id': selected_patient_id[0],
            'doctor_id': selected_doctor_id[0],
            'appointment_date': str(appointment_date),
            'appointment_time': str(appointment_time),
            'consultation_type': consultation_type
        }
        response = requests.post('http://127.0.0.1:5000/appointments', json=new_appointment)
        if response.status_code == 201:
            st.success('Appointment created successfully!')
        else:
            st.error(f'Error creating appointment: {response.status_code} - {response.text}')

def main():
    st.title("Medical Management System")
    menu = st.sidebar.selectbox("Select an option", ["Create Appointment", "Create Prescription"])

    if menu == "Create Appointment":
        create_appointment()

if __name__ == "__main__":
    main()

    
if menu == "Doctors":
    show_doctors()
elif menu == "Patients":
    show_patients()
elif menu == "Appointments":
    show_appointments()
elif menu == "Patient Prescriptions":
    show_prescriptions()
elif menu == "Add Doctor":
    add_doctor()
elif menu == "Add Patient":
    add_patient()
elif menu == "Add Medication":
    add_medication()
elif menu == "Create Prescription":
    create_prescription()
elif menu == "Prescription Medications":
    show_prescription_medications()
