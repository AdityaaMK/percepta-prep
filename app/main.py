from h11._abnf import status_code
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status

from app import database, schemas

app = FastAPI(
    title="Healthcare Notes System",
    description="A simplified API for managing patient clinical notes",
    version="1.0.0"
)

@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"message": "Welcome to the Healthcare Notes System API"}

@app.get("/notes", response_model=List[schemas.NoteResponse], status_code=status.HTTP_200_OK)
def get_notes(patient_id: Optional[str] = None):
    """
    Retrieve all notes. Optionally filter by patient_id.
    """
    return database.get_all_notes(patient_id=patient_id)

@app.get("/notes/{note_id}", response_model=schemas.NoteResponse, status_code=status.HTTP_200_OK)
def get_note(note_id: int):
    """
    Retrieve a specific note by its ID.
    """
    # BUG/ISSUE: database.get_note_by_id raises KeyError if it doesn't exist.
    # Because we don't handle KeyError here, FastAPI will return a 500 Internal Server Error
    # instead of a 404 Not Found.
    note = database.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note

@app.post("/notes", response_model=schemas.NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(payload: schemas.NoteCreate):
    """
    Create a new note. Notes are initialized as unsigned (signed=False).
    """
    note = database.create_note(
        patient_id=payload.patient_id,
        clinician_id=payload.clinician_id,
        text=payload.text
    )
    return note

# create new sign post endpoint
@app.post("/notes/{note_id}/sign", response_model=schemas.NoteResponse, status_code=status.HTTP_200_OK)
def sign_note(note_id: int):
    """
    sign a note by its ID.
    """
    note = get_note(note_id)
    if note["signed"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="note is already signed")
    note = database.update_note_sign(note_id)
    return note

@app.put("/notes/{note_id}", response_model=schemas.NoteResponse, status_code=status.HTTP_200_OK)
def update_note(note_id: int, payload: schemas.NoteUpdate):
    """
    update a note
    """
    note = get_note(note_id)
    if note["signed"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot update a signed note")
    note["text"] = payload.text
    return note
    





