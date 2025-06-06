from fastapi.testclient import TestClient
import sys
import os
# Ensuring parent directory is in sys.path so 'main' can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app  # your FastAPI app

client = TestClient(app)

def test_rental_report_format():
    response = client.get("/library_report")
    assert response.status_code == 200
    data = response.json()
    if data:
        for book_title, info in data.items():
            assert "book_id" in info
            assert "user_id" in info
            assert "borrowed_date" in info
            assert "days_borrowed" in info
            assert "days_overdue" in info

