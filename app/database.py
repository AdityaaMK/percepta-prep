import datetime
from typing import Dict, List, Optional

# Simulated database
# Structured as a dictionary mapping note_id (int) -> note dict
DB_NOTES: Dict[int, dict] = {
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
}

_next_id = 3

def get_all_notes(patient_id: Optional[str] = None) -> List[dict]:
    notes = list(DB_NOTES.values())
    if patient_id:
        notes = [n for n in notes if n["patient_id"] == patient_id]
    return notes

def get_note_by_id(note_id: int) -> dict:
    # BUG/ISSUE: If note_id doesn't exist, this raises KeyError.
    # In main.py, this is not caught and results in FastAPI returning a 500 Internal Server Error,
    # instead of a proper 404 Not Found.
    return DB_NOTES.get(note_id)

def create_note(patient_id: str, clinician_id: str, text: str) -> dict:
    global _next_id
    
    # BUG/ISSUE: Timezone-naive datetime is used here.
    # The application should use timezone-aware UTC datetime.
    now = datetime.datetime.now(datetime.timezone.utc)
    
    note = {
        "id": _next_id,
        "patient_id": patient_id,
        "clinician_id": clinician_id,
        "text": text,
        "signed": False,
        "created_at": now
    }
    DB_NOTES[_next_id] = note
    _next_id += 1
    return note

def update_note_sign(note_id):
    DB_NOTES[note_id]["signed"] = True
    return DB_NOTES[note_id]

def update_note_text(note_id: int, text: str) -> dict:
    # This function is not yet exposed via main.py, but will be used in Problem 3.
    # But wait, it doesn't check if the note is signed! 
    # Checking sign status should be handled in the API or database layer, 
    # and properly tested.
    note = get_note_by_id(note_id)
    note["text"] = text
    return note
