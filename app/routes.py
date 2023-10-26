# routes.py
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import RegistrationForm, LoginForm, EHRForm, AppointmentForm   # Import your registration and login forms
from app.models import User, EHR, Appointment   # Import your User and EHR models
from flask_login import current_user, login_user, logout_user, login_required
from app.blockchain import Blockchain

# EHM_RECORD = Blueprint('EHM_RECORD', __name__, template_folder='templates', static_folder='static')
# from . import EHM_RECORD



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)

        # Assign additional fields like full_name, date_of_birth, address, etc.
        user.full_name = form.full_name.data
        user.date_of_birth = form.date_of_birth.data
        user.address = form.address.data
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('register.html', title='Register', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'patient':
        ehr_records = EHR.query.filter_by(patient_id=current_user.id).all()
        return render_template('patient_dashboard.html', ehr_records=ehr_records, user=current_user)
    elif current_user.role == 'doctor':
        patients = User.query.filter_by(role='patient').all()
        appointments = Appointment.query.filter_by(doctor_id=current_user.id).all()
        return render_template('doctor_dashboard.html', patients=patients, appointments=appointments, user=current_user)
    return "Unsupported role"


@app.route('/logout')
@login_required  # Ensure the user is logged in to access this route
def logout():
    logout_user()
    flash('You have been logged out.')  # Optionally, display a message
    return redirect(url_for('login'))  # Redirect to the login page or any other page after logout


@app.route('/add_ehr', methods=['POST'])
@login_required
def add_ehr():
    if current_user.role == 'doctor':
        # Retrieve EHR data from the request (you may use a form)
        ehr_data = request.form.get('ehr_data')
        # Add EHR data to the blockchain
        blockchain = Blockchain()
        blockchain.add_ehr_to_blockchain(ehr_data)
        # Save EHR data in the database (SQLite) as well
        ehr = EHR(patient_id=current_user.id, medical_records=ehr_data)
        db.session.add(ehr)
        db.session.commit()
        flash('EHR record added to the blockchain and database.')
        return redirect(url_for('dashboard'))
    return "Unauthorized"

@app.route('/verify_ehr/<ehr_id>')
@login_required
def verify_ehr(ehr_id):
    if current_user.role == 'patient':
        # Convert ehr_id to an integer
        ehr_id = int(ehr_id)

        # Retrieve the EHR data from the blockchain and verify its integrity
        blockchain = Blockchain()
        ehr_data, is_valid = blockchain.verify_ehr(ehr_id)
        if is_valid:
            return render_template('patient_dashboard.html', ehr_data=ehr_data)
        else:
            flash('EHR data is tampered or invalid.')
            return redirect(url_for('dashboard'))
    return "Unauthorized"

# Add a route for doctors to view and modify patient EHR records
@app.route('/view_modify_ehr/<ehr_id>', methods=['GET', 'POST'])
@login_required
def view_modify_ehr(ehr_id):
    if current_user.role == 'doctor':
        ehr_record = EHR.query.get(ehr_id)
        if ehr_record:
            # Check if the patient has verified the doctor using the blockchain
            if ehr_record.patient_id == current_user.id:
                form = EHRForm()
                if form.validate_on_submit():
                    ehr_data = form.ehr_data.data
                    ehr_record.medical_records = ehr_data
                    db.session.commit()
                    flash('EHR record modified successfully.')
                    return redirect(url_for('doctor_dashboard'))
                return render_template('view_modify_ehr.html', ehr_record=ehr_record, form=form)
            else:
                return "Unauthorized to view or modify this EHR record"
        else:
            return "EHR record not found"
    return "Unsupported role"

@app.route('/schedule_appointment', methods=['GET', 'POST'])
@login_required
def schedule_appointment():
    if current_user.role == 'patient':
        form = AppointmentForm ()  # Replace 'YourAppointmentForm' with the actual form you're using

        # Retrieve the list of doctors and pass them as choices for the doctor_id field
        doctors = User.query.filter_by(role='doctor').all()
        form.doctor_id.choices = [(doctor.id, doctor.full_name) for doctor in doctors]


        if request.method == 'POST' and form.validate_on_submit():
            # Get data from the validated form
            doctor_id = form.doctor_id.data
            date = form.date.data
            time = form.time.data
            details = form.details.data

            # Here, you should add the time validation logic
            # if not is_valid_time(time):
            #     flash('Invalid appointment time. Please choose a valid time within working hours.')
            # else:
            # Create a new appointment
            appointment = Appointment(doctor_id=doctor_id, patient_id=current_user.id, date=date, time=time, details=details)

            # Add the appointment to the blockchain (example: blockchain.add_appointment(appointment))
            blockchain = Blockchain()
            blockchain.add_appointment(appointment)

            # Save the appointment to the database
            db.session.add(appointment)
            db.session.commit()
            flash('Appointment scheduled successfully!')

            return redirect(url_for('dashboard'))

        # Render the appointment scheduling form
        doctors = User.query.filter_by(role='doctor').all()
        return render_template('schedule_appointment.html', doctors=doctors, form=form)

    return "Unauthorized"


@app.route('/patient_profile/<int:patient_id>')
def patient_profile(patient_id):
    # Retrieve the patient's information from the database
    patient = User.query.get(patient_id)

    if patient:
        # If the patient is found, you can pass their information to the template
        return render_template('patient_profile.html', patient=patient)
    else:
        # Handle the case where the patient is not found
        return "Patient not found"



@app.route('/view_appointment_reports')
def view_appointment_reports():
    # Assuming that the current_user is a patient
    if current_user.role == 'patient':
        # Create an instance of the blockchain
        blockchain = Blockchain()

        # Retrieve the appointments from the blockchain
        appointments = blockchain.chain[1:]  # Assuming the first block is the genesis block

        # Filter appointments related to the current patient
        patient_appointments = [appointment for appointment in appointments if appointment.patient_id == current_user.id]

        # Fetch additional information about doctors
        doctors = User.query.filter_by(role='doctor').all()
        doctor_info = {doctor.id: doctor.username for doctor in doctors}

        # Render an HTML template to display the appointment reports
        return render_template('view_appointment_reports.html', patient_appointments=patient_appointments, doctor_info=doctor_info)
    else:
        flash('Unauthorized access.')  # Optional: Provide a flash message for unauthorized access
        return redirect(url_for('patient_dashboard'))

# Route for a patient to view their appointment reports
@app.route('/appointment_reports', methods=['GET'])
@login_required
def appointment_reports():
    if current_user.role == 'patient':
        # Query the database to retrieve the appointments made by the current patient
        appointments = Appointment.query.filter_by(patient_id=current_user.id).all()

        return render_template('appointment_reports.html', appointments=appointments)
    else:
        return "Unauthorized"


@app.route('/view_ehr/<int:ehr_id>', methods=['GET'])
@login_required  # Assuming you have login functionality
def view_ehr(ehr_id):
    if current_user.role == 'patient':
        ehr_record = EHR.query.get(ehr_id)

        if not ehr_record or ehr_record.patient_id != current_user.id:
            flash('EHR record not found or you do not have access to it.')
            return redirect(url_for('patient_dashboard'))

        return render_template('view_ehr.html', ehr_record=ehr_record)
    else:
        return "Unauthorized"


@app.route('/doctor_view_patient_ehr/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def doctor_view_patient_ehr(appointment_id):
    if current_user.role == 'doctor':
        # Retrieve the appointment based on the appointment_id
        appointment = Appointment.query.get(appointment_id)

        if not appointment or appointment.doctor_id != current_user.id:
            flash('Appointment not found or unauthorized access.')
            return redirect(url_for('doctor_dashboard'))

        # Retrieve the patient's EHR records
        ehr_records = EHR.query.filter_by(patient_id=appointment.patient_id).first()

        # Create an instance of your EHR form
        form = EHRForm(obj=ehr_records)  # Load EHR data into the form
        if form.validate_on_submit():
            if ehr_records is None:
                ehr_records = EHR(patient_id=appointment.patient_id)

            form.populate_obj(ehr_records)  # Update the EHR records object with form data
            db.session.add(ehr_records)  # Add the new EHR records or update existing
            db.session.commit()
            flash('EHR records updated successfully.')
            return redirect(url_for('dashboard'))

        return render_template('doctor_view_patient_ehr.html', form=form, appointment=appointment)
    else:
        return "Unauthorized"


@app.route('/doctor_view_patient_report/<int:appointment_id>')
@login_required
def doctor_view_patient_report(appointment_id):
    if current_user.role == 'doctor':
        # Retrieve the appointment based on the appointment_id
        appointment = Appointment.query.get(appointment_id)

        if not appointment or appointment.doctor_id != current_user.id:
            flash('Appointment not found or unauthorized access.')
            return redirect(url_for('doctor_dashboard'))

        # Retrieve the patient's EHR records
        ehr_records = EHR.query.filter_by(patient_id=appointment.patient_id).all()

        # You can now render an HTML template to display the patient's EHR records
        return render_template('doctor_view_patient_report.html', ehr_records=ehr_records, appointment=appointment)
    else:
        return "Unauthorized"


@app.route('/ehr_detail/<int:record_id>', methods=['GET'])
@login_required
def ehr_detail(record_id):
    ehr_record = EHR.query.get(record_id)

    if ehr_record is None:
        flash('EHR record not found.')
        return redirect(url_for('dashboard'))  # You can redirect to a suitable page

    # Render a template to display the details of the EHR record
    return render_template('ehr_detail.html', ehr_record=ehr_record)


# @app.route('/patient_dashboard')
# def patient_dashboard():
#     # Display the patient dashboard
#     return render_template('patient_dashboard.html')

# @app.route('/doctor_dashboard')
# def doctor_dashboard():
#     # Display the doctor dashboard
#     return render_template('doctor_dashboard.html')
