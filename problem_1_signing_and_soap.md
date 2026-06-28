# Problem 1: Feature Implementation (Signing and Filtering)
**Suggested Time Limit: 15 minutes**

## Objective
Implement two new features: note signing and filtering notes by patient.

---

## Tasks

### Task A: Note Signing Endpoint
You need to allow clinicians to finalize a note by "signing" it.
* **HTTP Method & URL**: `POST /notes/{note_id}/sign`
* **Response**: Returns the updated note object with `signed: true`.
* **Behavior & Edge Cases**:
  * If the note ID does not exist, return a `404 Not Found` response with `{"detail": "Note not found"}`.
  * If the note is already signed, return a `400 Bad Request` response with `{"detail": "Note is already signed"}`.

### Task B: Filtering in GET /notes
Currently, `GET /notes` accepts an optional `patient_id` query parameter. Enhance this endpoint or ensure it is functioning correctly so that:
* It properly filters the returned notes by `patient_id` when the query parameter is provided.
* If no filter is provided, it returns all notes in the database.

---

## Instructions
1. Implement any necessary functions in [app/database.py](file:///Users/adityaamk/Desktop/percepta%20prep/app/database.py).
2. Create the new endpoint in [app/main.py](file:///Users/adityaamk/Desktop/percepta%20prep/app/main.py).
3. Write unit tests in [tests/test_main.py](file:///Users/adityaamk/Desktop/percepta%20prep/tests/test_main.py) to verify:
   * A note can be successfully signed.
   * Attempting to sign a non-existent note returns 404.
   * Attempting to sign an already signed note returns 400.
4. Run your tests with `./venv/bin/pytest`.
