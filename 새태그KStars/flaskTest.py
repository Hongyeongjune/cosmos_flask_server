import os

from flask import Flask, jsonify
from flask import request

app = Flask(__name__)


@app.route("/cosmos/KStars/test", methods=['POST'])
def cosmos_load_file():
    data = request.json
    print(data)
    print(data)

    return jsonify(data)
