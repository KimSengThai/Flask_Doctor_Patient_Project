from flask import Blueprint, request, make_response, jsonify
from models import db, Doctor

doctor_bp = Blueprint('doctor', __name__, url_prefix="/doctors")

@doctor_bp.route('/')
def index():
    doctors_from_db = Doctor.query.all()
    doctors = [doctor.to_dict(rules=('-appointments.doctor',)) for doctor in doctors_from_db]
    return make_response(jsonify(doctors), 200)

@doctor_bp.route('/', methods=['POST'])
def create():
    new_doctor = Doctor(
        name=request.json.get('name'),
        specialization=request.json.get('specialization')
    )
    db.session.add(new_doctor)
    db.session.commit()

    if new_doctor.id:
        return make_response(jsonify(new_doctor.to_dict(rules=('-appointments.doctor',))), 201)

    return make_response(jsonify({"message": "Create unsuccessful!"}), 404)
