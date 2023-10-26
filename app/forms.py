# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, validators, TimeField # Import TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.fields import DateField
from wtforms.widgets import TextArea  # Import TextArea widget

from wtforms.widgets import TextArea  # Import TextArea widget

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message="Invalid email address")])
    role = SelectField('Role', choices=[('patient', 'Patient'), ('doctor', 'Doctor')], validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Register')

class EHRForm(FlaskForm):
    medical_records = TextAreaField('Medical Records', render_kw={"rows": 10, "cols": 50})
    diagnosis = TextAreaField('Diagnosis')
    prescriptions = TextAreaField('Prescriptions', render_kw={"rows": 5, "cols": 50})
    test_results = TextAreaField('Test Results', render_kw={"rows": 5, "cols": 50})
    allergies = TextAreaField('Allergies or Sensitivities', render_kw={"rows": 5, "cols": 50})
    immunization_records = TextAreaField('Immunization Records', render_kw={"rows": 5, "cols": 50})
    medical_history = TextAreaField('Detailed Medical History', render_kw={"rows": 10, "cols": 50})
    procedures = TextAreaField('History of Medical Procedures', render_kw={"rows": 10, "cols": 50})
    lab_reports = TextAreaField('Laboratory Reports', render_kw={"rows": 10, "cols": 50})
    vitals = TextAreaField('Vital Signs Data', render_kw={"rows": 5, "cols": 50})
    notes = TextAreaField('Additional Medical Notes', render_kw={"rows": 5, "cols": 50})
    family_history = TextAreaField('Family Medical History', render_kw={"rows": 5, "cols": 50})
    social_history = TextAreaField('Social and Lifestyle History', render_kw={"rows": 5, "cols": 50})
    radiology_reports = TextAreaField('Radiology and Imaging Reports', render_kw={"rows": 10, "cols": 50})
    medications = TextAreaField('Current and Past Medications', render_kw={"rows": 5, "cols": 50})
    chief_complaint = TextAreaField('Chief Complaint')

    submit = SubmitField('Update EHR')


class AppointmentForm(FlaskForm):
    doctor_id = SelectField('Select Doctor', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    details = TextAreaField('Appointment Details', validators=[DataRequired()])
    submit = SubmitField('Schedule Appointment')

# class RequestEHRForm(FlaskForm):
#     patient_id = HiddenField('Patient ID', validators=[DataRequired()])
#     additional_data = TextAreaField('Additional Information')
#     submit = SubmitField('Request EHR')
