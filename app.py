from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Dummy data store with salary by month
employees = [
    {"id": 1, "name": "John Doe", "position": "Developer", "salaries": {"2024-11": 60000, "2024-12": 62000}},
    {"id": 2, "name": "Jane Smith", "position": "Manager", "salaries": {"2024-11": 80000, "2024-12": 82000}},
    {"id": 3, "name": "Emily Johnson", "position": "Designer", "salaries": {"2024-11": 55000, "2024-12": 57000}},
    {"id": 4, "name": "Michael Brown", "position": "Analyst", "salaries": {"2024-11": 45000, "2024-12": 46000}},
    {"id": 5, "name": "Sarah Wilson", "position": "Data Scientist", "salaries": {"2024-11": 90000, "2024-12": 92000}},
    {"id": 6, "name": "David Lee", "position": "Product Manager", "salaries": {"2024-11": 85000, "2024-12": 87000}},
    {"id": 7, "name": "Laura Martinez", "position": "HR Specialist", "salaries": {"2024-11": 50000, "2024-12": 51000}},
    {"id": 8, "name": "Robert White", "position": "Sales Lead", "salaries": {"2024-11": 75000, "2024-12": 76000}},
    {"id": 9, "name": "Mary Green", "position": "Marketing Manager", "salaries": {"2024-11": 65000, "2024-12": 67000}},
    {"id": 10, "name": "James Adams", "position": "Engineer", "salaries": {"2024-11": 70000, "2024-12": 72000}},
    {"id": 11, "name": "Patricia Clark", "position": "Operations Manager", "salaries": {"2024-11": 83000, "2024-12": 84000}},
    {"id": 12, "name": "Linda Lewis", "position": "UX Designer", "salaries": {"2024-11": 62000, "2024-12": 63000}},
    {"id": 13, "name": "Barbara Walker", "position": "Content Strategist", "salaries": {"2024-11": 48000, "2024-12": 49000}},
    {"id": 14, "name": "Paul King", "position": "IT Support", "salaries": {"2024-11": 42000, "2024-12": 43000}},
    {"id": 15, "name": "Nancy Hall", "position": "Finance Analyst", "salaries": {"2024-11": 56000, "2024-12": 57000}}
]


# Helper function to find an employee by ID
def find_employee(emp_id):
    return next((emp for emp in employees if emp["id"] == emp_id), None)


# GET: Retrieve all employees with pagination
@app.route('/employees', methods=['GET'])
def get_employees():
    # Check if both 'page' and 'per_page' are provided
    page = request.args.get('page')
    per_page = request.args.get('per_page')

    if not page or not per_page:
        return jsonify({"error": "Both 'page' and 'per_page' query parameters are required"}), 400

    try:
        page = int(page)
        per_page = int(per_page)
    except ValueError:
        return jsonify({"error": "'page' and 'per_page' must be integers"}), 400

    start = (page - 1) * per_page
    end = start + per_page
    paginated_employees = employees[start:end]
    
    return jsonify(paginated_employees), 200


# GET: Retrieve an employee by ID and month (optional)
@app.route('/employees/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    month = request.args.get('month')
    employee = find_employee(emp_id)
    
    if not employee:
        abort(404, description="Employee not found")
    
    # If month is specified, return salary data for that month
    if month:
        salary = employee["salaries"].get(month)
        if salary:
            return jsonify({"id": emp_id, "name": employee["name"], "position": employee["position"], "month": month, "salary": salary}), 200
        else:
            return jsonify({"message": f"No salary data for {month}"}), 404
    
    return jsonify(employee), 200


# POST: Add a new employee
@app.route('/employees', methods=['POST'])
def create_employee():
    new_employee = request.get_json()
    new_employee["id"] = employees[-1]["id"] + 1 if employees else 1
    new_employee["salaries"] = new_employee.get("salaries", {})
    employees.append(new_employee)
    return jsonify(new_employee), 201


# PUT: Update an existing employee's salary for a specific month
@app.route('/employees/<int:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    employee = find_employee(emp_id)
    if not employee:
        abort(404, description="Employee not found")
    
    data = request.get_json()
    month = data.get("month")
    salary = data.get("salary")
    
    if not month or not salary:
        return jsonify({"error": "Month and salary are required fields"}), 400
    
    employee["salaries"][month] = salary
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
