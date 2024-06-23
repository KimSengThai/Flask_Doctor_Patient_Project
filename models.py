from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Doctor(db.Model, SerializerMixin):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    specialization = db.Column(db.String)

    appointments = db.relationship('Appointment', back_populates='doctor')
    patients = association_proxy('appointments', 'patient', creator=lambda p: Appointment(patient=p))

    # Exclude appointments to avoid recursion
    serializer_rules = ('-appointments.doctor',)
    # def to_json(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "specialization": self.specialization
    #     }

    def __repr__(self):
        return f"<Doctor {self.id}: {self.name} - {self.specialization}>"

class Patient(db.Model, SerializerMixin):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)

    appointments = db.relationship('Appointment', back_populates='patient')
    doctors = association_proxy('appointments', 'doctor', creator=lambda d: Appointment(doctor=d))

    # Exclude appointments to avoid recursion
    serializer_rules = ('-appointments.patient',)
    # def to_json(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "birthdate": str(self.birthdate)
    #     }

    def __repr__(self):
        return f"{self.id}: {self.name}"

class Appointment(db.Model, SerializerMixin):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    complaint = db.Column(db.String, nullable=False)

    doctor = db.relationship('Doctor', back_populates='appointments')
    patient = db.relationship('Patient', back_populates='appointments')

    # Exclude back references to avoid recursion
    serializer_rules = ('-doctor.appointments', '-patient.appointments')

    def __repr__(self):
        return f"Appointment {self.id}: {self.complaint}"
