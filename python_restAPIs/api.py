from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app =  Flask(__name__)
BASE = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE + 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db 
db = SQLAlchemy(app)

# Init marshmallow (serialization purpose)
ma = Marshmallow(app)

# Product Class/Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    position = db.Column(db.String(100))
    quote = db.Column(db.String(200))

    def __init__(self, name, age, position, quote):
        self.name = name
        self.age = age
        self.position = position
        self.quote = quote

# Employee schema
class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'age', 'position', 'quote')

# Init schema
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

# Endpoints
# POST
@app.route('/employees', methods=['POST'])
def AddEmployee():
    name = request.json['name']
    age = request.json['age']
    position = request.json['position']
    quote = request.json['quote']

    new_employee = Employee(name, age, position, quote)

    db.session.add(new_employee)
    db.session.commit()

    return employee_schema.jsonify(new_employee)

# Get all employees
@app.route('/employees', methods=['GET'])
def GetEmployees():
    all_employees = Employee.query.all()
    result = employees_schema.dump(all_employees)
    return jsonify(result)

# Get a specific Employee by ID
@app.route('/employees/<id>', methods=['GET'])
def GetEmployee(id):
    employee = Employee.query.get(id)
    return employee_schema.jsonify(employee)

# Update a specific Employee
@app.route('/employees/<id>', methods=['PATCH'])
def UpdateEmployee(id):
    employee = Employee.query.get(id)
 
    name = request.json['name']
    age = request.json['age']
    position = request.json['position']
    quote = request.json['quote']

    employee.name = name
    employee.age = age
    employee.position = position
    employee.quote = quote

    db.session.commit()

    return employee_schema.jsonify(employee)

# Run server
if __name__ == '__main__':
    app.run(debug=True)



    