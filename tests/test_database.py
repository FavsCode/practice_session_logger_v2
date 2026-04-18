""""Tests for the database module."""
import pytest
from pathlib import Path
from src.database import create_db

@pytest.fixture
def database_path(tmp_path: Path) -> Path:
    db_file = tmp_path / "test.sqlite"
    return db_file

def test_create_db_initializes_database(database_path: Path) -> None:
    create_db(path=database_path)
    assert database_path.exists()