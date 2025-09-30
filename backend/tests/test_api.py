import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_video():
    response = client.post("/api/v1/generate-video", json={
        "concept": "Une astuce pour mémoriser des noms",
        "n_images": 3,
        "category": "astuce",
        "lang": "fr"
    })
    assert response.status_code == 200
    assert "video_path" in response.json()
    assert response.json()["video_path"].endswith(".mp4")