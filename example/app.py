from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/create",  methods=['POST'])
def create():
    return {"message": "Embedding created"}


@app.route("/get", methods=['GET'])
def get():
    return {"embedding": "Here's the embedding"}


if __name__ == "__main__":
    app.run(debug=True)
