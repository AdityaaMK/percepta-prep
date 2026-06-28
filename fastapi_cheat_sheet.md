# FastAPI Cheat Sheet: Path vs Query Parameters & FastAPI Basics

## 1. Path vs Query Parameters

| Feature | Path Parameters | Query Parameters |
| :--- | :--- | :--- |
| **URL Appearance** | `/notes/12` | `/notes?patient_id=12` |
| **FastAPI Route** | `@app.get("/notes/{note_id}")` | `@app.get("/notes")` |
| **Required?** | Yes (the URL won't match without it) | Usually optional (can have default values) |
| **Typical Use Case** | Unique ID of a specific resource | Filtering, sorting, pagination, search queries |

### Path Parameters (Identify a Resource)
Path parameters are part of the actual URL path. Use them to locate a specific item.
```python
# The parameter name must match in the path and function signature
@app.get("/notes/{note_id}")
def get_note(note_id: int):
    return {"note_id": note_id}
```

### Query Parameters (Filter/Modify a List)
Query parameters appear after a `?` at the end of the URL. Use them to filter collections.
```python
# Parameters NOT specified in the route pattern are query parameters
@app.get("/notes")
def get_notes(patient_id: str = None, limit: int = 10):
    return {"patient_id": patient_id, "limit": limit}
```

---

## 2. FastAPI Basics for the Interview

### HTTP Exceptions
To return a specific HTTP status code (like 400 or 404), raise an `HTTPException` from `fastapi`:
```python
from fastapi import HTTPException, status

# Raise a 404 Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, 
    detail="Note not found"
)

# Raise a 400 Bad Request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, 
    detail="Cannot edit signed notes"
)
```

### Pydantic Validation (V2)
Define validation rules within Pydantic models. Custom field validation is done with `@field_validator`:
```python
from pydantic import BaseModel, Field, field_validator

class NoteCreate(BaseModel):
    patient_id: str
    clinician_id: str
    text: str = Field(..., min_length=1)

    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        # Strip leading and trailing whitespace
        stripped = v.strip()
        if not stripped:
            raise ValueError("Text cannot be empty or whitespace only")
        return stripped
```
*Note: Any raised `ValueError` or validation failure inside Pydantic automatically results in a `422 Unprocessable Entity` HTTP response from FastAPI.*

### Timezone-Aware Dates in Python
Avoid using timezone-naive datetime objects (like `utcnow()`). Instead, use timezone-aware UTC dates:
```python
import datetime

# Correct modern approach:
now = datetime.datetime.now(datetime.timezone.utc)
```

### Running Tests
Use `pytest` to run tests:
```bash
./venv/bin/pytest
```
In tests, use `client.post` or `client.put` with the `json` argument to send JSON bodies:
```python
response = client.post("/notes", json={"patient_id": "PAT-1", "text": "Hello"})
assert response.status_code == 201
assert response.json()["text"] == "Hello"
```
