
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Nurse Notes Sample API (5 notes)")

# Allow cross-origin for easy testing from other hosts (change in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

class Note(BaseModel):
    id: str
    patient_id: Optional[str]
    created_at: datetime
    note_date: str                # YYYY-MM-DD
    author_id: Optional[str]
    text: str                     # the nurse's note text
    status: str
    action_items: List[str] = []  # list of action-item details (strings)

# Five example nurse notes. Each includes nurse note text and action_items.
SAMPLE_NOTES = [
    Note(
        id="note-1",
        patient_id="patient-1001",
        created_at=datetime(2025, 9, 1, 8, 15),
        note_date="2025-09-01",
        author_id="nurse-a",
        text="Patient reported mild chest pain after walking. Vitals stable. Advised rest and monitoring.",
        status="new",
        action_items=[
            "Monitor vitals every 30 minutes for 2 hours.",
            "If chest pain persists, escalate to physician and order ECG."
        ]
    ),
    Note(
        id="note-2",
        patient_id="patient-1002",
        created_at=datetime(2025, 9, 1, 9, 30),
        note_date="2025-09-01",
        author_id="nurse-b",
        text="Post-op patient showing slight fever (38.1C). Given paracetamol per orders. Will recheck in 2 hours.",
        status="new",
        action_items=[
            "Administer paracetamol 500 mg as ordered.",
            "Recheck temperature in 2 hours and document response."
        ]
    ),
    Note(
        id="note-3",
        patient_id="patient-1003",
        created_at=datetime(2025, 9, 2, 7, 50),
        note_date="2025-09-02",
        author_id="nurse-c",
        text="Patient with diabetes checking blood glucose: 220 mg/dL. Insulin sliding scale given as per protocol.",
        status="new",
        action_items=[
            "Record blood glucose every 4 hours.",
            "Follow insulin sliding scale; notify physician if > 300 mg/dL."
        ]
    ),
    Note(
        id="note-4",
        patient_id="patient-1004",
        created_at=datetime(2025, 9, 2, 11, 5),
        note_date="2025-09-02",
        author_id="nurse-a",
        text="Patient reports dizziness when standing. Orthostatic BP measured; slight drop observed. Advised slow position changes.",
        status="new",
        action_items=[
            "Advise patient to stand slowly and call for assistance when needed.",
            "Document orthostatic BP measurements and report if symptomatic."
        ]
    ),
    Note(
        id="note-5",
        patient_id="patient-1001",
        created_at=datetime(2025, 9, 3, 10, 20),
        note_date="2025-09-03",
        author_id="nurse-b",
        text="Wound dressing changed; no signs of infection. Patient tolerating procedure well.",
        status="new",
        action_items=[
            "Continue daily wound dressing changes.",
            "Observe for erythema, drainage, or fever and notify clinician if present."
        ]
    ),
]

NOTES_BY_ID = {note.id: note for note in SAMPLE_NOTES}

@app.get("/api/v1/notes", response_model=List[Note])
async def list_notes():
    """Return the 5 sample nurse notes as JSON."""
    return SAMPLE_NOTES

@app.get("/api/v1/notes/{note_id}", response_model=Note)
async def get_note(note_id: str):
    """Return a single note by id."""
    note = NOTES_BY_ID.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "ok"}

# optional friendly root
@app.get("/", include_in_schema=False)
async def root():
    return {"service":"Nurse Notes Sample App", "docs":"/docs", "health":"/health"}
