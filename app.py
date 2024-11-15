from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Dummy data store
employees = [
    {"id": 1, "name": "John Doe", "position": "Developer", "salary": 60000},
    {"id": 2, "name": "Jane Smith", "position": "Manager", "salary": 80000},
    {"id": 3, "name": "Emily Johnson", "position": "Designer", "salary": 55000}
]


# Helper function to find an employee by ID
def find_employee(emp_id):
    return next((emp for emp in employees if emp["id"] == emp_id), None)


# GET: Retrieve all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees), 200


# GET: Retrieve an employee by ID
@app.route('/employees/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    employee = find_employee(emp_id)
    if employee:
        return jsonify(employee), 200
    else:
        abort(404, description="Employee not found")


# POST: Add a new employee
@app.route('/employees', methods=['POST'])
def create_employee():
    new_employee = request.get_json()
    new_employee["id"] = employees[-1]["id"] + 1 if employees else 1
    employees.append(new_employee)
    return jsonify(new_employee), 201


# PUT: Update an existing employee's salary
@app.route('/employees/<int:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    employee = find_employee(emp_id)
    if not employee:
        abort(404, description="Employee not found")
    
    data = request.get_json()
    employee.update({
        "name": data.get("name", employee["name"]),
        "position": data.get("position", employee["position"]),
        "salary": data.get("salary", employee["salary"])
    })
    return jsonify(employee), 200


# DELETE: Remove an employee by ID
@app.route('/employees/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    employee = find_employee(emp_id)
    if not employee:
        abort(404, description="Employee not found")
    
    employees.remove(employee)
    return jsonify({"message": "Employee deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
