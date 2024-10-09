from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "super secret key"

# Database connection configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'database': 'organ_donation'
}

# Home route rendering the homepage
@app.route('/')
def homepage():
    return render_template('index.html')

# Route for donor registration form
@app.route('/donor')
def donor():
    return render_template('donor-registration.html')

@app.route('/trans')
def trans():
    return render_template('transplant-matching.html')
@app.route('/vdonors')
def get_donors():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM donors")  # Replace with your actual table name
    donors = cursor.fetchall()
    cursor.close()
    conn.close()
    return donors

@app.route('/donors')
def donors():
    donor_list = get_donors()
    return render_template('donors.html', donors=donor_list)

if __name__ == '__main__':
    app.run(debug=True)


# Route to handle donor form submission
@app.route('/register_donor', methods=['POST'])
def register_donor():
    donor_fullname = request.form['DonorFullName']
    donor_age = request.form['DonorAge']
    donor_gender = request.form['gender']
    donor_medical_id = request.form['DonorMedicalID']
    donor_blood_type = request.form['bloodtype']
    donor_organs = request.form.getlist('Organ')
    donor_weight = request.form['DonorWeight']
    donor_height = request.form['DonorHeight']

    donor_organs_str = ', '.join(donor_organs)

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO donors (fullname, age, gender, medical_id, blood_type, organs, weight, height)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (donor_fullname, donor_age, donor_gender, donor_medical_id, donor_blood_type, donor_organs_str, donor_weight, donor_height))

        conn.commit()
        flash('Donor registered successfully!', 'success')
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('donor_form'))

# Route for patient registration form
@app.route('/patient')
def patient_form():
    return render_template('patient-registration.html')

# Route to handle patient form submission
@app.route('/register_patient', methods=['POST'])
def register_patient():
    patient_fullname = request.form['PatientFullName']
    patient_age = request.form['PatientAge']
    patient_gender = request.form['gender']
    patient_medical_id = request.form['PatientMedicalID']
    patient_blood_type = request.form['bloodtype']
    patient_organs = request.form.getlist('Organ')
    patient_weight = request.form['PatientWeight']
    patient_height = request.form['PatientHeight']

    patient_organs_str = ', '.join(patient_organs)

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO patients (fullname, age, gender, medical_id, blood_type, organs, weight, height)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (patient_fullname, patient_age, patient_gender, patient_medical_id, patient_blood_type, patient_organs_str, patient_weight, patient_height))

        conn.commit()
        flash('Patient registered successfully!', 'success')
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('patient_form'))

if __name__ == '__main__':
    app.run(debug=True)
