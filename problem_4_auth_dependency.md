# Problem 4: Authentication, Context Injection & Permissions
**Suggested Time Limit: 25 minutes**

## Objective
Implement dependency-injection-based authentication and enforce role-based access control.

---

## Background Context
We have added a set of mock clinicians to the database:
* `DR-SMITH` (Token: `token-smith-123`, Role: `clinician`)
* `DR-JONES` (Token: `token-jones-456`, Role: `clinician`)
* `DR-ADMIN` (Token: `token-admin-789`, Role: `admin`)

Only authenticated clinicians should be able to create, view, update, or sign notes. Additionally:
* A note's author is the clinician who created it.
* A note can only be updated or signed by:
  1. The clinician who created it (the author).
  2. Any clinician with the role `admin`.
* If a clinician tries to update/sign a note they do not own (and they are not an admin), the API must return `403 Forbidden`.

---

## Tasks

### Task A: Implement Security Dependency
Create a dependency function `get_current_clinician` in a new file or in [app/main.py](file:///Users/adityaamk/Desktop/percepta%20prep/app/main.py):
* It must look for an `Authorization` header containing `Bearer <token>`.
* Use FastAPI's `HTTPBearer` security utility (`from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials`).
* If the token is missing, invalid, or doesn't map to a clinician, raise `HTTPException(status_code=401, detail="Invalid or missing authentication token")`.
* If valid, return the clinician profile (e.g. dictionary with `id`, `name`, `role`).

### Task B: Inject Clinician into Note Creation
Update `POST /notes` to use the authentication dependency:
* Remove `clinician_id` from the request body schema [NoteCreate](file:///Users/adityaamk/Desktop/percepta%20prep/app/schemas.py#L14). Instead, the API should automatically set the note's `clinician_id` to the ID of the authenticated clinician.
* Route signature hint:
  ```python
  @app.post("/notes")
  def create_note(payload: NoteCreate, clinician: dict = Depends(get_current_clinician)):
  ```

### Task C: Enforce Permissions on Update and Sign
Update `PUT /notes/{note_id}` and `POST /notes/{note_id}/sign`:
* Require the `get_current_clinician` dependency on these endpoints.
* Verify permissions: if the authenticated clinician's `id` does not match the note's `clinician_id` AND the clinician's role is not `"admin"`, raise `403 Forbidden` (`raise HTTPException(status_code=403, detail="Permission denied")`).

---

## Verification
Failing tests have been appended to [tests/test_main.py](file:///Users/adityaamk/Desktop/percepta%20prep/tests/test_main.py) under the Section `PROBLEM 4`. Implement the authentication logic and verify they pass.
