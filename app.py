import os

from flask import Flask

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

@app.route("/")
def index():
    return "Hello, world!"

if __name__ == '__main__':
    app.run()
