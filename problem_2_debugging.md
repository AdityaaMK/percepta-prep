# Problem 2: Debugging and Edge Cases
**Suggested Time Limit: 10 minutes**

## Objective
Identify and resolve the three intentional bugs present in the codebase. Currently, running `./venv/bin/pytest` will show that 2 tests in the suite are failing.

---

## Tasks

### Task A: KeyError / HTTP 500 on Non-existent Note
* **Symptom**: Fetching a note that does not exist (`GET /notes/999`) returns a `500 Internal Server Error` instead of a `404 Not Found`.
* **Goal**: Modify the code so that it raises an appropriate exception or handles the `KeyError` from [app/database.py](file:///Users/adityaamk/Desktop/percepta%20prep/app/database.py) to return a `404 Not Found` response with `{"detail": "Note not found"}`.
* **Target File**: [app/main.py](file:///Users/adityaamk/Desktop/percepta%20prep/app/main.py) or [app/database.py](file:///Users/adityaamk/Desktop/percepta%20prep/app/database.py).

### Task B: Empty Text / Whitespace Note Validation
* **Symptom**: A clinician can create a note with empty text or whitespace (e.g. `"   "`), which is clinically invalid.
* **Goal**: Update the Pydantic schema so that creating a note with empty or whitespace-only text fails with a validation error (`422 Unprocessable Entity`).
* **Target File**: [app/schemas.py](file:///Users/adityaamk/Desktop/percepta%20prep/app/schemas.py).

### Task C: Timezone-Aware UTC Datetime
* **Symptom**: The note creation timestamp uses timezone-naive UTC time (`datetime.datetime.utcnow()`), which is deprecated in newer Python versions and does not explicitly declare its timezone.
* **Goal**: Update note creation to use timezone-aware UTC datetime.
* **Target File**: [app/database.py](file:///Users/adityaamk/Desktop/percepta%20prep/app/database.py).

---

## Instructions
1. Run `./venv/bin/pytest` and observe the failing tests.
2. Fix the bugs across [app/main.py](file:///Users/adityaamk/Desktop/percepta%20prep/app/main.py), [app/database.py](file:///Users/adityaamk/Desktop/percepta%20prep/app/database.py), and [app/schemas.py](file:///Users/adityaamk/Desktop/percepta%20prep/app/schemas.py).
3. Ensure all tests in [tests/test_main.py](file:///Users/adityaamk/Desktop/percepta%20prep/tests/test_main.py) pass.
