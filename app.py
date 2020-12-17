"""
RESTful API für Dr. W. CMS
RESTful API for Dr. W. CMS
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

# Initialisiere app / init app
app = Flask(__name__)
cors = CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
# Datenbank Konfiguration / db config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialisiere db / init db
db = SQLAlchemy(app)
# Initialisiere Marshmallow / init ma
ma = Marshmallow(app)

"""
Klasse, Schema von Öffnungszeiten
Class, Schema of Opening Times
"""

#Klasse Öffnungszeiten
class Times(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(100))
    day = db.Column(db.String(20), unique=True)

    def __init__(self, time, day):
        self.time = time
        self.day = day

#Schema Öffnungszeiten
class TimesSchema(ma.Schema):
    class Meta:
        fields = ('time', 'day')

"""
Klasse, Schema von Praxisteam
Class, Schema of Doctor and Employees
"""

#Klasse Mitarbeiter / Class Employee
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    about = db.Column(db.Text)

    def __init__(self, first_name, last_name, about):
        self.first_name = first_name
        self.last_name = last_name
        self.about = about

#Schema Mitarbeiter / Schema Employee
class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('first_name', 'last_name', 'about', 'id')


"""
Klasse, Schema von Kontakt
Class, Schema of Contact
"""

#Klasse Kontakt / Class Contact
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    street = db.Column(db.Text)
    number = db.Column(db.Integer)
    zip = db.Column(db.Integer)
    city = db.Column(db.String(40))
    phone = db.Column(db.String(40))

    def __init__(self, name, street, number, zip, city, phone):
        self.name = name
        self.street = street
        self.number = number
        self.zip = zip
        self.city = city
        self.phone = phone

#Kontakt Schema / Schema Contact
class ContactSchema(ma.Schema):
    class Meta:
        fields = ('name', 'street', 'number', 'zip', 'city', 'phone')


"""
Klasse, Schema Leistungen
Class, Schema of Services
"""

#Leistung Klasse / Service Class
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(20))
    heading2 = db.Column(db.String(30))
    text = db.Column(db.Text)


    def __init__(self, heading, heading2, text):
        self.heading = heading
        self.heading2 = heading2
        self.text = text

#Leistung Schema / Service Schema
class ServiceSchema(ma.Schema):
    class Meta:
        fields = ('heading', 'heading2', 'text', 'id')


"""
Initialisierung aller Schemas
Init of all schemas
"""

#Init Schmemas
time_schema = TimesSchema()
times_schema = TimesSchema(many=True)
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
contact_schema = ContactSchema()
service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)


"""
Alle RESTful Endpunkte bzgl. Öffnungszeiten
All RESTful endpoints for opening and closing times
"""

#Erstelle Öffnungszeiten / Create (POST) opening and closing times
#!!!! Nicht verwenden !!!!! Nur verwenden wenn neue Datenbank erstellt wurde !!!
#!!!! DO NOT USE !!!! ONLY USE IF DATABASE IS DESTROYED OR NEEDS TO BE RENEWED
@app.route('/create_opening_times', methods=['POST'])
def add_time():
    time = request.json['time']
    day = request.json['day']

    new_time = Times(time, day)

    db.session.add(new_time)
    db.session.commit()

    return time_schema.jsonify(new_time)

#Alle  Öffnungszeiten / GET opening and closing times from monday to friday
@app.route('/get_all_times', methods=['GET'])
def get_all_times():

  all_times = Times.query.all()

  result = times_schema.dump(all_times)

  return jsonify(result)

#Aktualisiere Öffnungszeiten mittels ID / Update (PUT) opening times with ID
# 1 - Montag; 2 - Dienstag; 3 - Mittwoch; 4 - Donnerstag; 5 - Freitag
@app.route('/update_time_<id>', methods=['PUT'])
def update_time(id):
    data = Times.query.get(id)

    day = request.json['day']
    time = request.json['time']

    data.day = day
    data.time = time

    db.session.commit()

    return time_schema.jsonify(data)


"""
Alle RESTful Endpunkte bzgl. Praxisteam
All RESTful endpoints for doctor and employees
"""

#Erstelle Praxisteam Mitglied
#Create (POST) doctor or employee
@app.route('/add_employee', methods=['POST'])
def add_employee():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    about = request.json['about']

    new_employee = Employee(first_name, last_name, about)

    db.session.add(new_employee)
    db.session.commit()

    return employee_schema.jsonify(new_employee)

#Gesamtes Praxisteam
#GET all data about doctor and employees
@app.route('/get_all_employees', methods=['GET'])
def get_all_employees():

    data = Employee.query.all()

    result = employees_schema.dump(data)

    return jsonify(result)

#Aktualisiere Daten zum Mitarbeiter oder Doktor mittels ID
#ID ist im JSON eines jeden GET-MITARBEITER Endpunktes zu sehen
#Update data about employee or doctor with ID
#(ID will be visible in JSON-DATA of GET-EMPLOYEE endpoints)
@app.route('/update_employee_<id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get(id)

    first_name = request.json['first_name']
    last_name = request.json['last_name']
    about = request.json['about']

    employee.first_name = first_name
    employee.last_name = last_name
    employee.about = about

    db.session.commit()

    return employee_schema.jsonify(employee)

#Lösche Mitarbeiter oder Doktor mittels ID
#ID ist im JSON eines jeden GET-MITARBEITER Endpunktes zu sehen
#Delete doctor or employee
#ID will be visible in JSON-DATA of GET-EMPLOYEE endpoints
@app.route('/delete_employee_<id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()

    return employee_schema.jsonify(employee)


"""
Alle RESTful Endpunkte bzgl. Kontaktdaten
All RESTful Endpoints for contact data
"""

#Erstelle Kontaktdaten
#!!!! Nicht verwenden !!!!! Nur verwenden wenn neue Datenbank erstellt wurde !!!
#Create Contact Data
#!!!! DO NOT USE !!!! ONLY USE IF DATABASE IS DESTROYED OR NEEDS TO BE RENEWED !!!
@app.route('/add_contact_data', methods=['POST'])
def add_contact():
    name = request.json['name']
    street = request.json['street']
    number = request.json['number']
    zip = request.json['zip']
    city = request.json['city']
    phone = request.json['phone']

    new_contact = Contact(name, street, number, zip, city, phone)

    db.session.add(new_contact)
    db.session.commit()

    return contact_schema.jsonify(new_contact)

#Kontaktdaten
#GET Contact Data
@app.route('/get_contact_data', methods=['GET'])
def get_contact():
    data = Contact.query.get(1)
    result = contact_schema.dump(data)
    return jsonify(result)

#Erneuere Kontaktdaten
#Update (PUT) Contact Data
@app.route('/update_contact_data', methods=['PUT'])
def update_contact():
    data = Contact.query.get(1)

    name = request.json['name']
    street = request.json['street']
    number = request.json['number']
    zip = request.json['zip']
    city = request.json['city']
    phone = request.json['phone']

    data.name = name
    data.street = street
    data.number = number
    data.zip = zip
    data.city = city
    data.phone = phone

    db.session.commit()

    return contact_schema.jsonify(data)

"""
Alle RESTful Endpunkte bzgl. Leistungen
All RESTful Endpoints for services
"""

#Erstelle Leistung
#Create Service
@app.route('/add_service', methods=['POST'])
def add_service():

    heading = request.json['heading']
    heading2 = request.json['heading2']
    text = request.json['text']

    new_service = Service(heading, heading2, text)

    db.session.add(new_service)
    db.session.commit()

    return service_schema.jsonify(new_service)

#Alle Leistungen
#GET all Services
@app.route('/get_all_services', methods=['GET'])
def get_all_services():
    all_services = Service.query.all()
    result = services_schema.dump(all_services)
    return jsonify(result)

#Aktualisiere Leistung mittels ID
#ID ist im JSON eines jeden GET-SERVICE Endpunktes zu sehen
#Update (PUT) Service with ID
#ID will be visible in JSON-DATA of GET-SERVICE endpoints
@app.route('/update_service_<id>', methods=['PUT'])
def update_service(id):

    service = Service.query.get(id)

    heading = request.json['heading']
    heading2 = request.json['heading2']
    text = request.json['text']

    service.heading = heading
    service.heading2 = heading2
    service.text = text

    db.session.commit()

    return service_schema.jsonify(service)

#Lösche Leistung mittels ID
#ID ist im JSON eines jeden GET-SERVICE Endpunktes zu sehen
#Delete Service with ID
#ID will be visible in JSON-DATA of GET-SERVICE endpoints
@app.route('/delete_service_<id>', methods=['DELETE'])
def delete_service(id):
    service = Service.query.get(id)
    db.session.delete(service)
    db.session.commit()

    return service_schema.jsonify(service)


"""
Server Konf. / Server Conf.
"""

# Starte Server / Setze debug auf false, wenn fertig implementiert
# Run Server / Set debug to false when in production
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
