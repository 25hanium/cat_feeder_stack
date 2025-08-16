import os
from fastapi import Header, HTTPException
from contextlib import contextmanager
from .database import SessionLocal

API_KEY = os.getenv("API_KEY")

def require_api_key(x_api_key: str | None = Header(default=None)):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Server API key not configured")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="invalid api key")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
