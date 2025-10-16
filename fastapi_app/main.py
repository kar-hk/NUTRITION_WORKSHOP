# fastapi_app/main.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from shared.db import Base, engine
import shared.models as models
from datetime import date

app = FastAPI(title='Nutrition Workshop — FastAPI example')
Base.metadata.create_all(bind=engine)  # dev convenience

class ParticipantCreate(BaseModel):
    name: str
    dob: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[str] = None

@app.post('/participants', status_code=201)
def create_participant(payload: ParticipantCreate):
    from shared.db import SessionLocal
    db = SessionLocal()
    try:
        p = models.Participant(name=payload.name, dob=payload.dob, phone=payload.phone, email=payload.email)
        db.add(p)
        db.commit()
        db.refresh(p)
        return {'id': p.id, 'name': p.name}
    finally:
        db.close()

@app.get('/health')
def health():
    return {'status': 'ok'}
