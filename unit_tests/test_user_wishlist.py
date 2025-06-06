from fastapi.testclient import TestClient
import sys
import os
# Ensuring parent directory is in sys.path so 'main' can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app  # your FastAPI app

client = TestClient(app)

def test_add_to_wishlist():
    response = client.post("/wishlist?user_id=4", json={
        "book_titles": ["The Lovely Bones"], "action": "add"
    })
    assert response.status_code == 200

def test_remove_from_wishlist():
    client.post("/wishlist?user_id=4", json={
        "book_titles": ["The Lovely Bones"], "action": "add"
    })  # First add
    response = client.post("/wishlist?user_id=4", json={
        "book_titles": ["The Lovely Bones"], "action": "remove"
    })
    assert response.status_code == 200
    assert "The Hobbit" not in response.json()["wishlist"]

def test_get_empty_wishlist():
    response = client.get("/wishlist?user_id=999")
    assert response.status_code == 200
    assert response.json()["wishlist"] == []
