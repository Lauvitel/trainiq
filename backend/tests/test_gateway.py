from fastapi.testclient import TestClient
from backend.gateway.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "TrainIQ Gateway API is running"}
