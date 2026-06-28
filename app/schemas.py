from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class NoteUpdate(BaseModel):
    text: str
    @field_validator('text')
    @classmethod
    def check_test_is_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("string is empty")
        return value

class NoteCreate(BaseModel):
    patient_id: str = Field(..., description="The unique identifier for the patient")
    clinician_id: str = Field(..., description="The unique identifier for the clinician")
    text: str = Field(..., description="The content of the clinical note")
    @field_validator('text')
    @classmethod
    def check_text_is_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("string is empty")
        return value

class NoteResponse(BaseModel):
    id: int
    patient_id: str
    clinician_id: str
    text: str
    signed: bool
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "patient_id": "PAT-101",
                "clinician_id": "DR-SMITH",
                "text": "Patient reports mild headache. Advised rest.",
                "signed": True,
                "created_at": "2026-06-27T10:00:00Z"
            }
        }
