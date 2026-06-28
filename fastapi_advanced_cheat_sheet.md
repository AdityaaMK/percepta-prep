# FastAPI Advanced Cheat Sheet: Dependency Injection, Async/Background Tasks, and Pydantic V2

## 1. FastAPI Dependency Injection (`Depends`)
Dependencies allow you to extract common logic (like security, DB sessions, or parameter extraction) and run it before your route handler is called.

### Declaring a Security Dependency
FastAPI provides utilities to extract credentials from headers. Use `HTTPBearer` for token authorization:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials  # Extract the token string
    
    # Perform validation
    user = mock_user_lookup(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return user
```

### Injecting into route operations
Simply add the dependency to your endpoint parameter signature:
```python
@app.post("/notes")
def create_note(payload: NoteCreate, user: dict = Depends(get_current_user)):
    # 'user' is the return value of get_current_user()
    return {"message": "Created", "user_id": user["id"]}
```

---

## 2. Pydantic V2 Advanced Validations

### Cross-Field Validation (`@model_validator`)
Use `@model_validator(mode='after')` to validate conditions that depend on multiple fields. The validator receives the entire model instance.
```python
from typing import Optional
from pydantic import BaseModel, model_validator

class AppointmentCreate(BaseModel):
    is_telehealth: bool
    video_link: Optional[str] = None

    @model_validator(mode='after')
    def validate_telehealth_fields(self) -> 'AppointmentCreate':
        # Self contains all attributes after they are individually validated
        if self.is_telehealth and not self.video_link:
            raise ValueError("Video link is required for telehealth appointments")
        return self
```
*Note: Returning `self` is mandatory in `mode='after'` validators.*

### String Constraints & Regex Patterns (`Field`)
You can restrict strings to match specific regular expressions using `pattern`:
```python
from pydantic import BaseModel, Field

class Patient(BaseModel):
    # Matches PAT-101, PAT-123456
    patient_id: str = Field(..., pattern=r"^PAT-\d{3,6}$")
```

---

## 3. Concurrency: `async def` vs `def` & Background Tasks

### Async vs Sync Path Operations
* **Use `def`** for blocking/synchronous code (like standard DB libraries, file operations, or raw CPU tasks). FastAPI executes sync functions in an internal threadpool so they don't block the main event loop.
* **Use `async def`** for non-blocking I/O (like calling another API using `httpx.AsyncClient` or querying an async database like `asyncpg`). Use `await` inside these functions. Never run a blocking call (like `time.sleep()`) inside `async def` as it freezes the entire API.

### FastAPI Background Tasks
Use `BackgroundTasks` to respond quickly to a request and run slow processing asynchronously.
```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

def slow_email_sender(email: str, message: str):
    # Some slow blocking call
    import time
    time.sleep(5)
    print(f"Sent: {message} to {email}")

@app.post("/contact")
def contact(email: str, background_tasks: BackgroundTasks):
    # Adds the task to the queue to run after the HTTP response is sent
    background_tasks.add_task(slow_email_sender, email, "Thank you for contacting us!")
    return {"message": "Received! Processing your inquiry."}
```

---

## 4. Overriding Dependencies in Pytest
When writing tests, you often want to mock authentication or database dependencies to avoid hitting real providers. Use `app.dependency_overrides`:

```python
from fastapi.testclient import TestClient
from app.main import app, get_current_user

client = TestClient(app)

# 1. Define a mock dependency
def mock_get_current_user():
    return {"id": "DR-MOCK", "role": "clinician"}

# 2. Apply the override in tests
def test_secured_endpoint():
    app.dependency_overrides[get_current_user] = mock_get_current_user
    
    response = client.post("/notes", json={"text": "Hello"})
    assert response.status_code == 201
    
    # 3. Clean up the overrides after the test
    app.dependency_overrides.clear()
```
