

from flask import Flask, jsonify, render_template
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/pie")
def color():

    data = [{
        "labels": ['Red', 'Green', 'Gold'],
        "values": [50,20,30],
        "type": "pie"}]

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
