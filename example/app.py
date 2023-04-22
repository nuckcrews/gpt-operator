import json
from uuid import uuid4
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def quarterback():
    return "Quarterbacks operation"


@app.route("/add",  methods=['POST'])
def create_quarterback():
    data = request.data.decode('utf-8')
    obj = json.loads(data)
    quarterback = obj.get('qb')

    if not quarterback:
        return {"error": "missing `quarterback` argument"}

    id = str(uuid4())
    qbs = []
    with open('data.json', mode='w', encoding='utf-8') as qbs_obj:
        qbs.append({
            "id": id,
            "quarterback": quarterback
        })
        json.dump(qbs, qbs_obj)

    return {"message": f"QB added with ID: {id}"}, 202


@app.route("/get", methods=['GET'])
def get_quarterback():
    id = request.args.get("qb")

    with open('data.json', 'r') as qbs_obj:
        obj = json.loads(qbs_obj.read())
        for qb in obj:
            if qb.get("id") == id:
                return qb, 200

@app.route("/search", methods=['GET'])
def search_quarterback():
    quarterback = request.args.get("qb").lower()

    with open('data.json', 'r') as qbs_obj:
        obj = json.loads(qbs_obj.read())
        for qb in obj:
            if qb.get("quarterback").lower() == quarterback:
                return qb, 200

    return {"error": "QB does not exist"}, 200


if __name__ == "__main__":
    app.run(debug=True)
