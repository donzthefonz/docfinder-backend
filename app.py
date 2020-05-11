import werkzeug
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Resource, Api, fields
from flask_cors import CORS, cross_origin
import smtplib, ssl

import logging
logging.basicConfig(level=logging.INFO, filename='../debug.log')

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doctors.sqlite3'
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)

GMAIL_PORT = 465  # For SSL
GMAIL_PASSWORD = "794613pa55"  # would normally keep in .env
GMAIL_FROM_EMAIL = "adatestap@gmail.com"


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
            # Get doctors data
            doctors = Doctor.query.all()
            docs = []
            for doc in doctors:
                doc_dict = doc.as_dict()
                docs.append(doc_dict)
            return {'Code': 200,
                    'doctors': docs}

        except Exception as e:
            print(str(e))
            logging.error(e)
            return {'Code': 500,
                    'Message': str(e)}


@api.route('/appointment')
class Appointment(Resource):
    # Send an email confirmation to the user
    def post(self):
        try:
            # Parse
            name = request.values.get('name')
            doctor = request.values.get('doctor')
            time = request.values.get('time')
            email = request.values.get('email')

            message = """ Hello {}. Your appointment with {} at {} has been accepted. """.format(name, doctor,
                                                                                                 time)
            # Send email
            # Create a secure SSL context
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com", GMAIL_PORT, context=context) as server:
                server.login(GMAIL_FROM_EMAIL, GMAIL_PASSWORD)
                server.sendmail(GMAIL_FROM_EMAIL, email, message)

            return {'Code': 200}

        except Exception as e:
            print(str(e))
            logging.error(e)
            return {'Code': 500,
                    'Message': str(e)}


if __name__ == '__main__':
    app.run()
