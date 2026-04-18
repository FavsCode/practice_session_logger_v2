"""Tests for the session module."""
import pytest
from datetime import datetime
from pathlib import Path
from src.session import Session, create_session, read_sessions, see_last_session, update_session, delete_session
from src.database import create_db

@pytest.fixture
def database_path(tmp_path: Path) -> Path:
    db_file = tmp_path / "test.sqlite"
    return db_file

@pytest.fixture
def test_data() -> list[Session]:
    session_1 = Session(date = "2026-02-20",
                        duration= 60, 
                        focus= "Repetition")
    session_2 = Session(date = "2026-03-21", 
                        duration= 30, 
                        focus= "Scales")
    session_3 = Session(date = "2026-04-22", 
                        duration= 45)
    test_data = [session_1, session_2, session_3]
    return test_data

def create_test_sessions(database_path: Path, test_data: list[Session]) -> None:
    create_db(path=database_path)

    for session in test_data:
        create_session(session,
                       path=database_path)
        
def test_create_session_creates_session(database_path: Path, test_data: list[dict]) -> None:
    create_db(path=database_path)

    session_1 = test_data[0]
    
    creation = create_session(session_1, path=database_path)
        
    sessions = read_sessions(path=database_path)

    assert creation == "Session successfully created."
    assert len(sessions) == 1

    stored = sessions[0]

    assert stored[1] == "2026-02-20"
    assert stored[2] == 60
    assert stored[3] == "Repetition"
    assert stored[4] == None

def test_read_sessions_returns_list_of_sessions(database_path: Path, test_data: list[Session]) -> None:
    create_test_sessions(database_path, test_data)

    sessions = read_sessions(path=database_path)

    assert len(sessions) == 3
    # Don't forget the ID indexing!
    # Indexing will start at zero, but ID will start at 1
    # Don't forget the Notes row as None!
    assert sessions[0] == (1, "2026-02-20", 60, "Repetition", None)
    assert sessions[1] == (2, "2026-03-21", 30, "Scales", None)
    assert sessions[2] == (3, "2026-04-22", 45, "No Focus", None)

def test_update_session_changes_session_data(database_path: Path, test_data: list[Session]) -> None:
    create_test_sessions(database_path, test_data)

    update_session("duration", 90, "2026-02-20", database_path)
    update_session("notes", "Good practice.", "2026-03-21", database_path)
    update_session("date", "2026-04-23", "2026-04-22", database_path)
    update_session("focus", "Recreation", "2026-02-20", database_path)

    sessions = read_sessions(path=database_path)

    assert sessions[0] == (1, "2026-02-20", 90, "Recreation", None)
    assert sessions[1] == (2, "2026-03-21", 30, "Scales", "Good practice.")
    assert sessions[2] == (3, "2026-04-23", 45, "No Focus", None)

def test_delete_session_deletes_session_data(database_path: Path, test_data: list[Session]) -> None:
    create_test_sessions(database_path, test_data)

    delete_session("2026-03-21", path=database_path)

    sessions = read_sessions(path=database_path)

    assert len(sessions) == 2
    assert sessions[0] == (1, "2026-02-20", 60, "Repetition", None)
    assert sessions[1] == (3, "2026-04-22", 45, "No Focus", None)

def test_last_session_returns_most_recent_session(database_path: Path, test_data: list[Session]) -> None:
    create_test_sessions(database_path, test_data)

    last_session = see_last_session(path=database_path)

    assert last_session == "Date: 2026-04-22, Duration: 45 minutes, Focus: No Focus, Notes: None"