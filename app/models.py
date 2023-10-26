# models.py

from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login_manager
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class EHR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    medical_records = db.Column(db.Text)
    diagnosis = db.Column(db.String(128))
    prescriptions = db.Column(db.Text)
    test_results = db.Column(db.Text)
    allergies = db.Column(db.Text)        # Allergies or sensitivities
    immunization_records = db.Column(db.Text)
    medical_history = db.Column(db.Text)  # Detailed medical history
    procedures = db.Column(db.Text)       # History of medical procedures
    lab_reports = db.Column(db.Text)      # Laboratory reports
    vitals = db.Column(db.Text)           # Vital signs data (e.g., blood pressure, heart rate)
    notes = db.Column(db.Text)            # Additional medical notes
    family_history = db.Column(db.Text)      # Family medical history
    social_history = db.Column(db.Text)      # Social and lifestyle history
    radiology_reports = db.Column(db.Text)   # Radiology and imaging reports
    medications = db.Column(db.Text)         # Current and past medications
    chief_complaint = db.Column(db.String(128))

    def __repr__(self):
        return f'<EHR {self.id}'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    full_name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    role = db.Column(db.String(32))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String(256))

    patient_ehr = db.relationship('EHR', foreign_keys=[EHR.patient_id], backref='patient', lazy='dynamic')
    doctor_ehr = db.relationship('EHR', foreign_keys=[EHR.doctor_id], backref='doctor', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}'
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)  # Date of the appointment
    time = db.Column(db.Time, nullable=False)  # Time of the appointment
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Patient ID
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Doctor ID
    details = db.Column(db.Text)  # Additional details or notes for the appointment
    doctor = db.relationship('User', foreign_keys=[doctor_id])
    patient = db.relationship('User', foreign_keys=[patient_id])
    def __repr__(self):
        return f'<Appointment {self.id}>'

    @property
    def formatted_datetime(self):
        return f'{self.date.strftime("%Y-%m-%d")} {self.time.strftime("%H:%M")}'

    def get_patient(self):
        return User.query.get(self.patient_id)

    def get_doctor(self):
        return User.query.get(self.doctor_id)

    # Additional methods for validation and data manipulation
    def validate_time(self):
        # Example validation: Ensure the appointment time is within working hours
        if self.time < datetime.strptime("08:00:00", "%H:%M:%S").time() or self.time > datetime.strptime("18:00:00", "%H:%M:%S").time():
            return False
        return True

    def calculate_duration(self):
        # Calculate the duration of the appointment
        return 30  # Assuming 30 minutes for each appointment

    def update_details(self, new_details):
        # Update the appointment details
        self.details = new_details
        db.session.commit()

    def reschedule(self, new_date, new_time):
        # Reschedule the appointment to a new date and time
        self.date = new_date
        self.time = new_time
        db.session.commit()

    def cancel(self):
        # Cancel the appointment
        self.status = 'canceled'
        db.session.commit()

    def mark_as_completed(self):
        # Mark the appointment as completed
        self.status = 'completed'
        db.session.commit()
