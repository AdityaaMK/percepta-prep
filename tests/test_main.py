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
            "created_at": datetime.datetime(2026, 6, 26, 10, 0, 0),
            "summary": None
        },
        2: {
            "id": 2,
            "patient_id": "PAT-102",
            "clinician_id": "DR-SMITH",
            "text": "Routine checkup. Blood pressure is 120/80. Heart rate 72 bpm.",
            "signed": False,
            "created_at": datetime.datetime(2026, 6, 27, 9, 30, 0),
            "summary": None
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
# THE FOLLOWING TESTS ARE PART OF THE COMPLETED EXERCISES
# =====================================================================

def test_get_nonexistent_note_404():
    """
    Problem 2 task: fetching a non-existent note should return 404.
    """
    response = client.get("/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

def test_create_note_validation_empty_text():
    """
    Problem 2 task: creating a note with empty text should return 422 Unprocessable Entity.
    """
    payload = {
        "patient_id": "PAT-103",
        "clinician_id": "DR-JONES",
        "text": "   "
    }
    response = client.post("/notes", json=payload)
    assert response.status_code == 422

# =====================================================================
# PROBLEM 4: AUTHENTICATION AND ROLE-BASED ACCESS CONTROL (RBAC)
# =====================================================================

def test_create_note_unauthenticated_fails():
    payload = {
        "patient_id": "PAT-103",
        "text": "Valid note text"
    }
    response = client.post("/notes", json=payload)
    assert response.status_code == 401

def test_create_note_authenticated_success():
    payload = {
        "patient_id": "PAT-103",
        "text": "Valid note text"
    }
    headers = {"Authorization": "Bearer token-smith-123"}
    response = client.post("/notes", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["clinician_id"] == "DR-SMITH"

def test_update_note_forbidden_for_non_author():
    payload = {"text": "Updated content"}
    # Note 2 is created by DR-SMITH. Let's try to update using DR-JONES.
    headers = {"Authorization": "Bearer token-jones-456"}
    response = client.put("/notes/2", json=payload, headers=headers)
    assert response.status_code == 403

def test_update_note_allowed_for_admin():
    payload = {"text": "Admin override"}
    # Note 2 is owned by DR-SMITH. Let's update using DR-ADMIN.
    headers = {"Authorization": "Bearer token-admin-789"}
    response = client.put("/notes/2", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["text"] == "Admin override"

# =====================================================================
# PROBLEM 5: BACKGROUND TASKS
# =====================================================================

def test_background_task_summary_generation():
    payload = {
        "patient_id": "PAT-103",
        "text": "Patient has severe cough."
    }
    headers = {"Authorization": "Bearer token-smith-123"}
    response = client.post("/notes", json=payload, headers=headers)
    assert response.status_code == 201
    note_id = response.json()["id"]
    
    # Under Starlette TestClient, background tasks run synchronously when response completes.
    # Check if summary got generated automatically
    get_resp = client.get(f"/notes/{note_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["summary"] == "Summary of note: Patient has seve..."

# =====================================================================
# PROBLEM 6: ADVANCED PYDANTIC VALIDATION & SOAP NOTES
# =====================================================================

def test_invalid_patient_id_pattern():
    payload = {
        "patient_id": "PAT-12",  # Too short, pattern requires 3-6 digits
        "text": "Valid note text"
    }
    headers = {"Authorization": "Bearer token-smith-123"}
    response = client.post("/notes", json=payload, headers=headers)
    assert response.status_code == 422

def test_create_soap_note_without_plan_or_assessment():
    payload = {
        "patient_id": "PAT-103",
        "subjective": "Headache",
        "objective": "BP 120/80"
    }
    headers = {"Authorization": "Bearer token-smith-123"}
    response = client.post("/notes/soap", json=payload, headers=headers)
    assert response.status_code == 201

def test_create_soap_note_with_plan_but_no_assessment_fails():
    payload = {
        "patient_id": "PAT-103",
        "subjective": "Headache",
        "objective": "BP 120/80",
        "plan": "Take ibuprofen"
    }
    headers = {"Authorization": "Bearer token-smith-123"}
    response = client.post("/notes/soap", json=payload, headers=headers)
    assert response.status_code == 422
    assert "Cannot have a Plan without an Assessment" in response.text

