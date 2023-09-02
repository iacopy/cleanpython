"""
Test the flask app
"""

# 3rd party
import pytest

# My stuff
from flask_app import app


@pytest.fixture
def client():
    """
    Create a test client using the Flask application configured for testing.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:  # pylint: disable=redefined-outer-name
        yield client


def test_hello(client):  # pylint: disable=redefined-outer-name
    """
    Test the hello page.
    """
    response = client.get("/hello")
    assert response.status_code == 200
    assert b"Hello from Flask!" in response.data


def test_index_get(client):  # pylint: disable=redefined-outer-name
    """
    Test the index page, GET method: only check the title.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>Elaborazione Codice</title>" in response.data


def test_index_post(client):  # pylint: disable=redefined-outer-name
    """
    Test the index page, POST method: check the title and the output.
    """
    response = client.post("/", data={"code": "print('hello world')"})
    assert response.status_code == 200
    assert b"<title>Elaborazione Codice</title>" in response.data
    assert b"<pre>PRINT(&#39;HELLO WORLD&#39;)</pre>" in response.data
