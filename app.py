import werkzeug
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Resource, Api, fields
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doctors.sqlite3'
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)


# Would normally put this in a models file
class Doctor(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(50))
    city = db.Column(db.String(30))
    postcode = db.Column(db.String(10))
    lat = db.Column(db.String(8))
    lng = db.Column(db.String(8))

    def __init__(self, name, address, city, postcode):
        self.name = name
        self.address = address
        self.city = city
        self.postcode = postcode

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Uncomment this to create the database if it does not exist or is out of date.
# db.create_all()

api = Api(app,
          version='0.1', title='DocFinder API', description='API for DocFinder')


@api.route('/healthcheck')
class HelloWorld(Resource):
    def get(self):
        return {"message": "alive"}


@api.route('/doctors')
class Doctors(Resource):
    def get(self):
        try:
            # Get doctors data and return
            doctors = Doctor.query.all()
            docs = []
            for doc in doctors:
                doc_dict = doc.as_dict()
                docs.append(doc_dict)
            return {'code': 200,
                    'doctors': docs}

        except Exception as e:
            return {'Code': 500,
                    'Message': str(e)}

    def post(self):
        try:
            # Send an email to the user
            email = request.form.get('email')
            doctor_name = request.form.get('doctor_name')
            time = request.form.get('time')
            email = request.form.get('email')

            # Send email

            return {'code': 200}

        except Exception as e:
            return {'Code': 500,
                    'Message': str(e)}


if __name__ == '__main__':
    app.run()
