import io
import json

import pytest

from app import app as flask_app  # Import your Flask app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_request_without_file(client):
    response = client.post("/api/exif")
    expected_data = {"message": "No file part in the request"}
    assert response.status_code == 400
    assert json.loads(response.data) == expected_data


def test_request_with_file(client):
    data = {}
    data['image'] = (io.BytesIO(b"abcdef"), 'test.jpg')
    response = client.post("/api/exif", data=data)
    assert response.status_code == 200
