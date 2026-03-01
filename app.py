
from flask import Flask, jsonify, request
from src.backend.persistence import bmi_db_helper
from src.backend.core.bmi_calculator import bmi_calculator, get_bmi_category
from flask import render_template

#initialize app
def create_app():
    app = Flask(__name__,
                static_folder="src/ui",
                static_url_path="/src/ui",
                template_folder="src/ui/templates")
    bmi_db_helper.init_db()

    return app

app = create_app()

#register routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/add-user', methods=['POST'])
def create_bmi_user():
    data = request.get_json()

    required_fields = ['name','email', 'age', 'height_cm', 'weight_kg','city', 'state']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Required fields are missing'}), 400

    bmi = bmi_calculator(data['height_cm'], data['weight_kg'])
    category = get_bmi_category(bmi)

    record = {
        'name': data['name'],
        'email': data['email'],
        'age': data['age'],
        'height_cm': data['height_cm'],
        'weight_kg': data['weight_kg'],
        'bmi': bmi,
        'bmi_category': category,
        'city': data['city'],
        'state': data['state']
    }

    record_id = bmi_db_helper.insert_user(record)

    return jsonify(
        {
            'id': record_id,
            'name': data['name'],
            'bmi': bmi,
            'bmi_category': category,
         }
    ), 201

@app.route("/bmi", methods=["GET"])
def get_all_bmi():
    records = bmi_db_helper.fetch_all()
    if not records:
        return jsonify({"message": "No users found"})
    print("Fetched records:", records)
    return jsonify(records)


@app.route("/bmi/<int:record_id>", methods=["GET"])
def get_bmi(record_id):
    record = bmi_db_helper.fetch_by_id(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    return jsonify(record)

@app.route("/bmi/<int:record_id>", methods=["PATCH"])
def update_data(record_id):
    print("Updating record with ID:", record_id)
    record = bmi_db_helper.fetch_by_id(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    data = request.get_json()
    updated_fields = {}

    for field in ['name', 'email', 'age', 'height_cm', 'weight_kg', 'city', 'state']:
        if field in data:
            updated_fields[field] = data[field]

    if 'height_cm' in updated_fields or 'weight_kg' in updated_fields:
        height_cm = updated_fields.get('height_cm', record['height_cm'])
        weight_kg = updated_fields.get('weight_kg', record['weight_kg'])
        bmi = bmi_calculator(height_cm, weight_kg)
        category = get_bmi_category(bmi)
        updated_fields['bmi'] = bmi
        updated_fields['bmi_category'] = category
    bmi_db_helper.update_record(record_id, updated_fields)

    return jsonify(
        {
            'id': record_id,
            'name': data['name'],
            'bmi': bmi,
            'bmi_category': category,
         }
    ), 201

@app.route("/bmi/<int:record_id>", methods=["DELETE"])
def delete_bmi(record_id):
    print("Deleting record with ID:", record_id)
    record = bmi_db_helper.fetch_by_id(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404

    bmi_db_helper.delete_record(record_id)
    return jsonify({"message": "Record deleted"})

#run server (backend)
if __name__ == "__main__":
    app.run(debug=True)
