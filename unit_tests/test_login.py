from fastapi.testclient import TestClient
import sys
import os
# Ensuring parent directory is in sys.path so 'main' can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app  # your FastAPI app

client = TestClient(app)

def test_login_success():
    response = client.post("/login", json={"email": "sam.richards@fca_user.com", "password": "Neon_Tide77"})
    assert response.status_code == 200
    assert "Login successful" in response.json()["message"]

def test_login_wrong_password():
    response = client.post("/login", json={"email": "sam.richards@fca_user.com", "password": "wrong_password"})
    assert response.status_code == 401

def test_login_nonexistent_user():
    response = client.post("/login", json={"email": "unknown@example.com", "password": "anything"})
    assert response.status_code == 404
