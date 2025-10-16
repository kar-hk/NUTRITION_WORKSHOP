# tests/test_basic.py
import os
from shared.db import engine, Base, SessionLocal
import shared.models as models
import pytest

def setup_module(module):
    # Use SQLite in-memory for tests to avoid needing MySQL in CI
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine_test = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(bind=engine_test)
    module.engine_test = engine_test
    module.SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

def test_participant_create():
    db = SessionTest()
    p = models.Participant(name='Test User')
    db.add(p)
    db.commit()
    db.refresh(p)
    assert p.id is not None
    assert p.name == 'Test User'
