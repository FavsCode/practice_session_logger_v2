"""This module contains the Session dataclass and functions to create, read, update, and delete sessions. It is the service layer of the application."""
from dataclasses import dataclass
from datetime import date, datetime
from os import path
from pathlib import Path
from .database import insert_session, delete_session as db_delete_session, update_session as db_update_session, select_sessions

@dataclass
class Session:
    date: date
    duration: int
    focus: str = "No Focus"
    notes: str | None = None
    id: int | None = None
    
    def __post_init__(self):
        if not isinstance(self.date, date):
            raise ValueError("Date must be a date object.")
        if not isinstance(self.duration, int):
            raise ValueError("Duration must be an integer.")
        if not isinstance(self.focus, str):
            raise ValueError("Focus must be a string.")
        if self.focus == "":
            self.focus = "No Focus"
        if self.notes is not None and not isinstance(self.notes, str):
            raise ValueError("Notes must be a string or None.")
        
def check_date_format(date_str: str) -> date | bool:
    """Checks if the date string is in the correct format."""
    try:
        user_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return user_date
    except ValueError:
        return False

def create_session(date: str,
                   duration: int,
                   focus: str = "No Focus", 
                   notes: str | None = None, 
                   id: int | None = None,
                   path: Path | None = None) -> str:
    """Creates new session with user-inputted information."""
    if not check_date_format(date):
        return "Error: Invalid date format."
    
    user_date = check_date_format(date)
    
    try: 
        duration = int(duration)
    except ValueError:
        return "Error: Invalid duration format."
    try:
        focus = str(focus)
        if not focus:
            focus = "No Focus"
    except ValueError:
        return "Error: Invalid focus format."
    try:
        notes = str(notes) if notes is not None else None
    except ValueError:        
        return "Error: Invalid notes format."

    # User date is already validated, so this will not return an error.
    new_session = Session(date=user_date, # type: ignore
                          duration=duration, 
                          focus=focus, 
                          notes=notes, 
                          id=id) 
    
    if path:
        insert_session(new_session, path=path)
    else:
        insert_session(new_session)

    return "Session successfully created."

def read_sessions(path: Path | None) -> list[tuple]:
    """Reads out session data."""
    if not path:
        return select_sessions()
    else:
        return select_sessions(path=path)

def update_session(session_aspect: str, edit: str | int, date: str, path: None | Path) -> str:
    """Replaces a session's data with new user-inputted info."""
    valid = valid_session_aspect(session_aspect, edit)
    if valid is not True: # If valid is not True, it is an error message.
        return valid # type: ignore
    
    try:
        user_date = datetime.strptime(str(date), "%Y-%m-%d").date()
    except ValueError:
        return "Error: Invalid date format."

    if path:
        # update_session defaults to the regular database, but if a path is provided, it is a testing path.
        db_update_session(session_aspect, edit, user_date, path)
    else:
        db_update_session(session_aspect, edit, user_date) # ignore

    return "Session updated successfully."

def delete_session(date: str, path: None | Path) -> str:
    """Deletes a session's data."""
    user_date = check_date_format(date)
    if not user_date:
        return "\nError: Invalid date format."
    
    # User date is validated, so its value will not be False, so the type is ignored.
    if path:
        db_delete_session(date=user_date, path=path) # type: ignore
    else: 
        db_delete_session(date=user_date) # type: ignore

    return "Session deleted successfully."

def see_last_session(path: None | Path) -> str:
    """Returns the most recent session's data."""
    sessions = read_sessions(path)
    if not sessions:
        return "No sessions found."
    
    last_session = sessions[-1]
    return f"Date: {last_session[1]}, Duration: {last_session[2]} minutes, Focus: {last_session[3]}, Notes: {last_session[4]}"

def valid_session_aspect(session_aspect: str, aspect) -> str | bool:
    """Runs all tests on the session aspect to prove it is a valid value."""
    allowed_fields = {"duration", "focus", "notes", "date"}

    if session_aspect not in allowed_fields:
        return (f"Invalid session aspect: {session_aspect}. Allowed aspects are: {allowed_fields}")
    
    try:
        if session_aspect == "duration":
            aspect = int(aspect)
        elif session_aspect in {"focus", "notes", "date"}:
            aspect = str(aspect)
            if session_aspect == "focus" and aspect == "":
                aspect = "No Focus"
    except ValueError:
        return "Error: Invalid aspect format."
    
    return True