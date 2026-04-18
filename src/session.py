"""This module contains the Session dataclass and functions to create, read, update, and delete sessions. It is the service layer of the application."""
from datetime import date, datetime
from pathlib import Path
from .database import insert_session, delete_session as db_delete_session, update_session as db_update_session, select_sessions
from .models import Session

def check_date_format(date_str: str) -> date | bool:
    """Checks if the date string is in the correct format."""
    try:
        user_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return user_date
    except ValueError:
        return False

def create_session(Session,
                   path: Path | None = None) -> str:
    """Creates new session with user-inputted information."""
    if not check_date_format(Session.date):
        return "Error: Invalid date format."
    
    user_date = check_date_format(Session.date)
    Session.date = user_date # We are mutating the Session object to be a date object instead of a string.

    try: 
        Session.duration = int(Session.duration)
    except ValueError:
        return "Error: Invalid duration format."
    try:
        Session.focus = str(Session.focus)
        if not Session.focus:
            Session.focus = "No Focus"
    except ValueError:
        return "Error: Invalid focus format."
    try:
        Session.notes = str(Session.notes) if Session.notes is not None else None
    except ValueError:        
        return "Error: Invalid notes format."

    if path:
        insert_session(Session, path=path)
    else:
        insert_session(Session)

    return "Session successfully created."

def read_sessions(path: Path | None) -> list[tuple]:
    """Reads out session data."""
    if not path:
        return select_sessions()
    else:
        return select_sessions(path=path)

def update_session(session: Session, path: None | Path) -> str:
    """Replaces a session's data with new user-inputted info."""
    try:
        session.date = datetime.strptime(str(session.date), "%Y-%m-%d").date()
    except ValueError:
        return "Error: Invalid date format."

    if path:
        # update_session defaults to the regular database, but if a path is provided, it is a testing path.
        db_update_session(session, path)
    else:
        db_update_session(session) 

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

def get_session_by_date(date: str, path: None | Path) -> Session | None:
    """Returns a session object based on the date."""
    user_date = check_date_format(date)
    if not user_date:
        print("Error: Invalid date format.")
        return None
    
    sessions = read_sessions(path)
    for session in sessions:
        if session[1] == str(datetime.strptime(str(user_date), "%Y-%m-%d").date()): # session[1] is the date in the database, which is a string, so we convert the user_date to a string for comparison.
            return Session(date=datetime.strptime(str(session[1]), "%Y-%m-%d").date(), 
                           duration=session[2], 
                           focus=session[3], 
                           notes=session[4], 
                           id=session[0])
    
    print("Session not found.")
    return None