from flask import Flask, render_template, request, redirect, url_for, flash
from contextlib import closing
from db_connection import get_db_connection
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_doctors():
    try:
        with closing(get_db_connection()) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM doctors")
                return cursor.fetchall()
    except Exception as e:
        return []

def get_patients():
    try:
        with closing(get_db_connection()) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM patients")
                return cursor.fetchall()
    except Exception as e:
        return []

def get_appointments():
    try:
        with closing(get_db_connection()) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute('''
                    SELECT a.appointment_id, a.appointment_date, a.appointment_time, a.consultation_type,
                            d.first_name AS doctor_first_name, d.last_name AS doctor_last_name,
                            p.first_name AS patient_first_name, p.last_name AS patient_last_name
                    FROM medical_appointments a
                    JOIN doctors d ON a.doctor_id = d.id
                    JOIN patients p ON a.patient_id = p.patient_id
                ''')
                appointments = cursor.fetchall()
                for appointment in appointments:
                    if isinstance(appointment['appointment_time'], timedelta):
                        appointment['appointment_time'] = appointment['appointment_time'].total_seconds()
                return appointments
    except Exception as e:
        return []

def get_medications():
    try:
        with closing(get_db_connection()) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute('SELECT * FROM medications')
                return cursor.fetchall()
    except Exception as e:
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/doctors')
def doctors():
    doctors = get_doctors()
    return render_template('doctors.html', doctors=doctors)

@app.route('/patients')
def patients():
    patients = get_patients()
    return render_template('patients.html', patients=patients)

@app.route('/appointments')
def appointments():
    appointments = get_appointments()
    return render_template('appointments.html', appointments=appointments)

@app.route('/medications')
def medications():
    medications = get_medications()
    return render_template('medications.html', medications=medications)

@app.route('/create_patient', methods=['POST'])
def create_patient():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    birth_date = request.form['birth_date']
    phone = request.form['phone']
    address = request.form['address']
    email = request.form['email']
    
    try:
        with closing(get_db_connection()) as conn:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO patients (first_name, last_name, birth_date, phone, address, email) VALUES (%s, %s, %s, %s, %s, %s)',
                                (first_name, last_name, birth_date, phone, address, email))
                conn.commit()
        flash("Patient created successfully.")
    except Exception as e:
        flash(f"Error creating patient: {str(e)}")
    
    return redirect(url_for('index'))

@app.route('/create_doctor', methods=['POST'])
def create_doctor():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    specialization = request.form['specialization']
    phone = request.form['phone']
    address = request.form['address']
    email = request.form['email']
    
    try:
        with closing(get_db_connection()) as conn:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO doctors (first_name, last_name, specialization, phone, address, email) VALUES (%s, %s, %s, %s, %s, %s)',
                                (first_name, last_name, specialization, phone, address, email))
                conn.commit()
        flash("Doctor created successfully.")
    except Exception as e:
        flash(f"Error creating doctor: {str(e)}")
    
    return redirect(url_for('doctors'))

@app.route('/create_medication', methods=['POST'])
def create_medication():
    name = request.form['name']
    description = request.form['description']
    
    try:
        with closing(get_db_connection()) as conn:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO medications (name, description) VALUES (%s, %s)',
                                (name, description))
                conn.commit()
        flash("Medication created successfully.")
    except Exception as e:
        flash(f"Error creating medication: {str(e)}")
    
    return redirect(url_for('medications'))

@app.route('/create_appointment', methods=['POST'])
def create_appointment():
    patient_id = request.form['patient_id']
    doctor_id = request.form['doctor_id']
    appointment_date = request.form['appointment_date']
    appointment_time = request.form['appointment_time']
    consultation_type = request.form['consultation_type']
    
    try:
        with closing(get_db_connection()) as conn:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO medical_appointments (patient_id, doctor_id, appointment_date, appointment_time, consultation_type) VALUES (%s, %s, %s, %s, %s)',
                                (patient_id, doctor_id, appointment_date, appointment_time, consultation_type))
                conn.commit()
        flash("Appointment created successfully.")
    except Exception as e:
        flash(f"Error creating appointment: {str(e)}")
    
    return redirect(url_for('appointments'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
