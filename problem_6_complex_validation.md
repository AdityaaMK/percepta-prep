# Problem 6: Complex Pydantic V2 Validation & Constraints
**Suggested Time Limit: 20 minutes**

## Objective
Implement advanced schema validations including regex constraints and cross-field dependency validation in Pydantic V2.

---

## Tasks

### Task A: Regex Pattern Constraint
Clinicians must assign notes to valid patient identifiers.
* Update `patient_id` in [NoteCreate](file:///Users/adityaamk/Desktop/percepta%20prep/app/schemas.py) and other schemas so that it must match the pattern `^PAT-\d{3,6}$` (e.g. `PAT-101` or `PAT-987654` are valid; `PAT-12` or `PAT-ABC` or `PAT-1234567` are invalid).
* In Pydantic V2, you can achieve this by using the `pattern` argument inside `Field()`:
  ```python
  patient_id: str = Field(..., pattern=r"^PAT-\d{3,6}$")
  ```

### Task B: Cross-Field Validation (Model Validator)
Clinicians sometimes create structured SOAP notes. We want to support structured inputs while enforcing logical healthcare rules:
* Create a new endpoint `POST /notes/soap` that takes a [SOAPNoteCreate](file:///Users/adityaamk/Desktop/percepta%20prep/app/schemas.py) request body:
  * Fields: `patient_id` (str), `subjective` (str), `objective` (str), `assessment` (Optional[str]), `plan` (Optional[str]).
* Enforce this rule: **A clinician cannot define a "Plan" if there is no "Assessment"**.
  * Use `@model_validator(mode='after')` inside the `SOAPNoteCreate` schema to check this condition.
  * If `plan` is provided and non-empty, but `assessment` is empty/null, raise a `ValueError("Cannot have a Plan without an Assessment")` (which FastAPI turns into a `422 Unprocessable Entity`).
  * Route signature:
    ```python
    @app.post("/notes/soap", response_model=schemas.NoteResponse, status_code=status.HTTP_201_CREATED)
    def create_soap_note(payload: schemas.SOAPNoteCreate, clinician: dict = Depends(get_current_clinician)):
        # Join sections into a single text note and create it in the database
        # text = f"S: {payload.subjective}\nO: {payload.objective}\nA: {payload.assessment or ''}\nP: {payload.plan or ''}"
    ```

---

## Verification
Tests have been added in [tests/test_main.py](file:///Users/adityaamk/Desktop/percepta%20prep/tests/test_main.py) under the `PROBLEM 6` section to verify valid/invalid patient IDs and model cross-field validation rules.
