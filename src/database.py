"""Contains operations on the SQLite database, such as creating the database, inserting, deleting, updating, and selecting session data."""
import sqlite3
from datetime import date
from pathlib import Path

def execute_command(sql: str, params: tuple=(), path: Path | str = 'practice_sessions.sqlite') -> None:
    """Connects to and executes commands on the SQLite database."""
    with sqlite3.connect(path) as sqlite_connection:
        cursor = sqlite_connection.cursor()
        cursor.execute(sql, params)
        sqlite_connection.commit()

def create_db(path: Path | str = '.practice_sessions.sqlite') -> None:
    """Initializes the SQLite database and creates the practice_sessions table if it doesn't exist."""
    sql ='''
        CREATE TABLE IF NOT EXISTS practice_sessions (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            duration INTEGER NOT NULL,
            focus TEXT,
            notes TEXT
        )
        '''
    execute_command(sql, path=path)

def insert_session(Session, path: Path | str = 'practice_sessions.sqlite') -> None:
    """Inserts session data to the database."""
    sql = '''
        INSERT INTO practice_sessions (date, duration, focus, notes) 
        VALUES (?, ?, ?, ?)
        '''
    params = (Session.date.isoformat(), Session.duration, Session.focus, Session.notes)
    execute_command(sql, params, path)

def delete_session(date: date, path: Path | str = 'practice_sessions.sqlite') -> None:
    """Deletes session data from the database."""
    sql = '''
        DELETE FROM practice_sessions
        WHERE date = ?
        '''
    params = (date.isoformat(),)
    execute_command(sql, params, path)

def update_session(session_aspect: str, edit: str | int, date: date, path: Path | str = 'practice_sessions.sqlite') -> None:
    """Updates session data from the database."""
    sql = f'''
        UPDATE practice_sessions
        SET {session_aspect} = ?
        WHERE date = ?
        '''
    params = (edit, date.isoformat())
    execute_command(sql, params, path)

def select_sessions(path: Path | str = 'practice_sessions.sqlite') -> list[tuple]:
    """Selects all session data from the database."""
    with sqlite3.connect(path) as sqlite_connection:
        cursor = sqlite_connection.cursor()
        cursor.execute('''
        SELECT * FROM practice_sessions
        ORDER BY id
        ''')
        return cursor.fetchall()