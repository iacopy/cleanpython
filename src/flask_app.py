"""
This is the main entry point for the Flask app.
"""
# 3rd party
from flask import Flask

# A very simple Flask Hello World app for you to get started with...
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello from Flask!"
