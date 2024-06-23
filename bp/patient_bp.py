from flask import Blueprint, request, make_response, jsonify
from models import db, Patient, Doctor, Appointment
from datetime import datetime

patient_bp = Blueprint('patient', __name__, url_prefix="/patients")

@patient_bp.route('/')
def index():
    patients_from_db = Patient.query.all()
    patients = [patient.to_dict(rules=('-appointments.patient',)) for patient in patients_from_db]
    return make_response(jsonify(patients), 200)

@patient_bp.route('/', methods=['POST'])
def create():
    birthdate = datetime.strptime(request.json['birthdate'], '%Y-%m-%d')
    new_patient = Patient(
        name=request.json.get('name'),
        birthdate=birthdate
    )
    db.session.add(new_patient)
    db.session.commit()

    if new_patient.id:
        return make_response(jsonify(new_patient.to_dict(rules=('-appointments.patient',))), 201)

    return make_response(jsonify({"message": "Create unsuccessful!"}), 404)

@patient_bp.route('/<int:patient_id>')
def show_by_id(patient_id):
    patient = Patient.query.filter(Patient.id == patient_id).first()
    if patient:
        return make_response(jsonify(patient.to_dict(rules=('-appointments.patient',))), 200)
    return make_response(jsonify({"error": "Patient not found"}), 404)

@patient_bp.route('/<int:patient_id>/consult_doctor', methods=['POST'])
def consult_doctor(patient_id):
    patient = Patient.query.filter(Patient.id == patient_id).first()
    if patient:
        doctor = Doctor.query.filter(Doctor.id == request.json['doctor_id']).first()
        if doctor:
            appointment = Appointment(patient_id=patient.id, doctor_id=doctor.id, complaint=request.json['complaint'])
            db.session.add(appointment)
            db.session.commit()

            if appointment.id:
                return make_response(jsonify({"message": "Appointment made!"}), 200)
        else:
            return make_response(jsonify({"message": "No Doctor found"}), 404)
    return make_response(jsonify({"message": "Patient not found"}), 404)
