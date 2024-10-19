from starlette.testclient import TestClient
from rag_refapp.main import app

client = TestClient(app)


def test_get_health():
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}


def test_get_database_health():
    response = client.get("/health/database")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}
