from flask import Flask # type: ignore
from flask_migrate import Migrate # type: ignore
from models import db
from bp.doctor_bp import doctor_bp
from bp.patient_bp import patient_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(doctor_bp)
app.register_blueprint(patient_bp)

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return "Welcome to the Hospital App"

if __name__ == "__main__":
    app.run(port=4000, debug=True)

