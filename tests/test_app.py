import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_status(client):
    response = client.get("/status")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "alive!"


def test_inference_invalid_input(mocker, client):
    data = {
        "SepalLengthCm": 5.1,
        "SepalWidthCm": 3.5,
        "PetalLengthCm": 1.4
    }
    response = client.post("/inference/", json=data)
    assert response.status_code == 400
    json_data = response.get_json()
    assert "error" in response.get_data(as_text=True).lower()


def test_inference_invalid_data_type(mocker, client):
    data = {
        "SepalLengthCm": "invalid",
        "SepalWidthCm": 3.5,
        "PetalLengthCm": 1.4,
        "PetalWidthCm": 0.2
    }
    response = client.post("/inference/", json=data)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error"] == "All values in the JSON must be numbers (float or int)."


def test_inference_invalid_data_feature(mocker, client):
    data = {
        "SepalLengthCm": 0.2,
        "SepalWidthCm": 3.5,
        "PetalLengthCm": 1.4,
        "random": 0.2
    }
    response = client.post("/inference/", json=data)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error"] == "The feature names should match those that were passed during fit."
