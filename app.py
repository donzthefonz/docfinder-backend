from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Resource, Api, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doctors.sqlite3'

db = SQLAlchemy(app)


# Would normally put this in a models file
class Doctor(db.Model):
    id = db.Column('doctor_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address1 = db.Column(db.String(50))
    address2 = db.Column(db.String(50))
    city = db.Column(db.String(30))
    postcode = db.Column(db.String(10))

    def __init__(self, name, address1, address2, city, postcode):
        self.name = name
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.postcode = postcode


# Uncomment this to create the database if it does not exist or is out of date.
db.create_all()

api = Api(app,
          version='0.1', title='DocFinder API', description='API for DocFinder')


@api.route('/healthcheck')
class HelloWorld(Resource):
    def get(self):
        return {"message": "alive"}


@api.route('/doctors')
class Device(Resource):
    def get(self):
        try:
            # TODO: Get doctors data and return
            doctor_data = []
            return {'code': 200,
                    'response': doctor_data}

        except Exception as e:
            return {'Code': 500,
                    'Response': str(e)}


if __name__ == '__main__':
    app.run()
