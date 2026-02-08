from unittest.mock import MagicMock
import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import db
# Mock init_db before importing main to prevent real DB connection attempt
db.init_db = MagicMock()

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from main import app
from db import get_session
import pytest

# Use in-memory SQLite for testing dependency override
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def get_session_override():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_session_override

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Todo API is running"}
