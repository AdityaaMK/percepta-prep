# Problem 3: API Evolution (Update Note Endpoint)
**Suggested Time Limit: 15 minutes**

## Objective
Implement an update (`PUT`) endpoint to edit notes and write unit tests for it.

---

## Tasks

### Task A: Implement PUT Endpoint
A clinician wants to correct errors in their note before it is finalized (signed).
* **HTTP Method & URL**: `PUT /notes/{note_id}`
* **Request Body**: A schema containing the updated `text` (e.g. `NoteUpdate` schema).
* **Response**: Returns the updated note object.
* **Behavior & Validation Rules**:
  * The updated text must not be empty or whitespace-only (respecting the same validation rules from Problem 2).
  * If the note is already signed, it **cannot** be edited. Return a `400 Bad Request` response with `{"detail": "Cannot update a signed note"}`.
  * If the note ID does not exist, return a `404 Not Found` response with `{"detail": "Note not found"}`.

### Task B: Write Tests
Write thorough unit tests in [tests/test_main.py](file:///Users/adityaamk/Desktop/percepta%20prep/tests/test_main.py) to cover all of the following scenarios:
1. Successfully updating an unsigned note.
2. Attempting to update a signed note (verifying it returns 400).
3. Attempting to update a non-existent note (verifying it returns 404).
4. Attempting to update a note with invalid/empty text (verifying it returns 422).

---

## Instructions
1. Define a Pydantic schema for the update request in [app/schemas.py](file:///Users/adityaamk/Desktop/percepta%20prep/app/schemas.py).
2. Wire up the database update and validation logic in [app/database.py](file:///Users/adityaamk/Desktop/percepta%20prep/app/database.py) and [app/main.py](file:///Users/adityaamk/Desktop/percepta%20prep/app/main.py).
3. Implement tests in [tests/test_main.py](file:///Users/adityaamk/Desktop/percepta%20prep/tests/test_main.py).
4. Run `./venv/bin/pytest` to verify your implementation.
