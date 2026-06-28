from httpx import ResponseNotRead
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import DB_NOTES

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    # Helper to reset database between tests to ensure test isolation
    import datetime
    global DB_NOTES
    DB_NOTES.clear()
    DB_NOTES.update({
        1: {
            "id": 1,
            "patient_id": "PAT-101",
            "clinician_id": "DR-SMITH",
            "text": "Patient reports mild headache. Advised rest and hydration.",
            "signed": True,
            "created_at": datetime.datetime(2026, 6, 26, 10, 0, 0)
        },
        2: {
            "id": 2,
            "patient_id": "PAT-102",
            "clinician_id": "DR-SMITH",
            "text": "Routine checkup. Blood pressure is 120/80. Heart rate 72 bpm.",
            "signed": False,
            "created_at": datetime.datetime(2026, 6, 27, 9, 30, 0)
        }
    })

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Healthcare Notes System API"}

def test_get_notes():
    response = client.get("/notes")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["patient_id"] == "PAT-101"

def test_get_notes_filter():
    response = client.get("/notes?patient_id=PAT-102")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["patient_id"] == "PAT-102"

def test_get_single_note():
    response = client.get("/notes/1")
    assert response.status_code == 200
    assert response.json()["patient_id"] == "PAT-101"

def test_sign_note():
    response = client.post("/notes/2/sign")
    assert response.status_code == 200

def test_sign_signed_note():
    response = client.post("/notes/1/sign")  
    assert response.status_code == 400

def test_create_note():
    payload = {
        "patient_id": "PAT-103",
        "clinician_id": "DR-JONES",
        "text": "Complaining of lower back pain."
    }
    response = client.post("/notes", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 3
    assert data["patient_id"] == "PAT-103"
    assert data["signed"] is False
    assert "created_at" in data

def test_update_unsigned_note():
    payload = {
        "text": "test"
    }
    response = client.put("/notes/2", json=payload)
    assert response.status_code == 200
    assert response.json()["text"] == "test"

def test_update_signed_note():
    payload = {
        "text": "test"
    }
    response = client.put("/notes/1", json=payload)
    assert response.status_code == 400

def test_update_null_note():
    payload = {
        "text": "test"
    }
    response = client.put("/notes/3", json=payload)
    assert response.status_code == 404 

def test_update_empty_note():
    payload = {
        "text": "  "
    }
    response = client.put("/notes/2", json=payload)
    assert response.status_code == 422 

# =====================================================================
# THE FOLLOWING TESTS ARE EXPECTED TO FAIL CURRENTLY (PART OF PROBLEMS)
# =====================================================================

def test_get_nonexistent_note_404():
    """
    Problem 2 task: fetching a non-existent note should return 404.
    Currently, it raises a KeyError in app/database.py and returns HTTP 500.
    """
    response = client.get("/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

def test_create_note_validation_empty_text():
    """
    Problem 2 task: creating a note with empty text should return 422 Unprocessable Entity.
    Currently, it allows empty text or whitespace.
    """
    payload = {
        "patient_id": "PAT-103",
        "clinician_id": "DR-JONES",
        "text": "   "
    }
    response = client.post("/notes", json=payload)
    assert response.status_code == 422
