"""
This is the main entry point for the Flask app.
"""
# 3rd party
from flask import Flask
from flask import render_template
from flask import request

# A very simple Flask Hello World app for you to get started with...
app = Flask(__name__)


@app.route("/hello")
def hello_world():
    """
    A simple route that returns a string.
    """
    return "Hello from Flask!"


@app.route("/", methods=["GET", "POST"])
def index():
    """
    The index page, with a form to submit code for processing.
    """
    if request.method == "POST":
        user_code = request.form["code"]
        output = user_code.upper()
        return render_template("index.html", output=output)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
