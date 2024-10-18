from starlette.testclient import TestClient
from rag_refapp.main import app

client = TestClient(app)


def test_get_ingest():
    response = client.get("/ingest/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}