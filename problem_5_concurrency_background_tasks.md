# Problem 5: Concurrency and Background Tasks
**Suggested Time Limit: 20 minutes**

## Objective
Implement asynchronous background processing for note clinical summaries to offload slow operations from the request-response loop.

---

## Background Context
In medical systems, running complex tasks like AI-based note summarization, coding (ICD-10 classification), or generating PDF clinical reports can take several seconds. If run directly inside the request handler, the API would hang, resulting in a poor user experience or timeout errors.

FastAPI provides a `BackgroundTasks` class that allows you to schedule a function to run *after* returning the response to the client.

---

## Tasks

### Task A: Implement the Async Worker
In [app/database.py](file:///Users/adityaamk/Desktop/percepta%20prep/app/database.py) or a helper module, write an asynchronous worker function:
```python
import asyncio

async def generate_note_summary(note_id: int):
    # Simulate a slow process (e.g. LLM summarization)
    await asyncio.sleep(2)
    # Update the note in DB_NOTES by setting a new field "summary" 
    # value: "Summary of note: <first 15 characters of note text>..."
```

### Task B: Integrate BackgroundTasks in note creation
Update `POST /notes` in [app/main.py](file:///Users/adityaamk/Desktop/percepta%20prep/app/main.py):
* Add `background_tasks: BackgroundTasks` as a parameter to the path operation.
* When a note is created, add the task to the queue:
  ```python
  background_tasks.add_task(generate_note_summary, note.id)
  ```
* Return the created note immediately. It should initially have `summary: None`.
* Add `summary: Optional[str] = None` to the [NoteResponse](file:///Users/adityaamk/Desktop/percepta%20prep/app/schemas.py) schema.

---

## Verification
Tests have been added under the `PROBLEM 5` section in [tests/test_main.py](file:///Users/adityaamk/Desktop/percepta%20prep/tests/test_main.py) which call `POST /notes`, assert that the response comes back instantly, wait for 2.1 seconds, and then fetch the note again to verify that the `summary` field is now populated.
