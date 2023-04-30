import json
from uuid import uuid4
from flask import Flask, request

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return "Quarterbacks API"


# Add a new quarterback
@app.route("/add",  methods=['POST'])
def create_quarterback():
    data = request.data.decode('utf-8')
    obj = json.loads(data)
    quarterback_name = obj.get('quarterback')

    if not quarterback_name:
        return {"error": "missing `quarterback` argument"}

    qb_id = str(uuid4())

    quarterbacks = []
    with open('data.json', 'r') as qbs_file:
        quarterbacks = json.loads(qbs_file.read())

    with open('data.json', mode='w', encoding='utf-8') as file:
        quarterbacks.append({
            "id": qb_id,
            "quarterback": quarterback_name
        })
        json.dump(quarterbacks, file)

    return {"message": f"Quarterback added with ID: {qb_id}"}, 202


# Get a quarterback by ID
@app.route("/get", methods=['GET'])
def get_quarterback():
    qb_id = request.args.get("id")

    with open('data.json', 'r') as qbs_file:
        qb_list = json.loads(qbs_file.read())
        for qb in qb_list:
            if qb.get("id") == qb_id:
                return qb, 200

    return {"error": "Quarterback not found"}, 404


# Search for a quarterback by name
@app.route("/search", methods=['GET'])
def search_quarterback():
    quarterback_name = request.args.get("quarterback").lower()

    with open('data.json', 'r') as qbs_file:
        qb_list = json.loads(qbs_file.read())
        for qb in qb_list:
            if qb.get("quarterback").lower() == quarterback_name:
                return qb, 200

    return {"error": "Quarterback not found"}, 404


if __name__ == "__main__":
    app.run(debug=True)