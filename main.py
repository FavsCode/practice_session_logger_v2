"""Entry point for the Practice Logger."""
from src.database import create_db
from src.session import get_session_by_date, create_session, read_sessions, update_session, delete_session, see_last_session
from src.models import Session

def divider() -> None:
    """Prints a divider line for better readability."""
    print("\n" + "-" * 40 + "\n")

def greet() -> None:
    """Prints a welcome message to the user."""
    print("Welcome to Practice Logger Mini!")
    print("An app that allows you to log and retrieve practice session data.\n")

    print("Your last session:")
    print(see_last_session(None) + "\n")

def menu() -> None:
    """Displays the main menu.
    """
    print("Menu:")
    print("1. Add session"
          "\n2. View sessions"
          "\n3. Update session"
          "\n4. Delete session"
          "\n5. Exit")
    divider()

def view_sessions() -> None:
    """Displays all sessions."""
    sessions = read_sessions(None) # Error with no input for some reason, so it's set to None
    if sessions:
        divider()
        print("Sessions:")
        for session in sessions:
            print(f"\nDate: {session[1]}, Duration: {session[2]} minutes, Focus: {session[3]}, Notes: {session[4]}")
        divider()
    else:
        print("\nNo sessions found.")
        divider()

def selection_add() -> None:
    """Handles the logic for adding a new session."""
    example_input = "2023-09-15, 60, Scales, Nice major scales!"
    print(f"\nExample input: {example_input}")
    print("Note: Notes are optional. If you don't have any notes, just leave that part blank.")

    create_session_input = input("Enter session details (date in YYYY-MM-DD format, duration in minutes, focus, notes - optional) separated by commas: ")
    try:
        date, duration, focus, notes = [item.strip() for item in create_session_input.split(",")]
    except ValueError: # A ValueError would raise if the user doesn't input the notes.
        date, duration, focus = [item.strip() for item in create_session_input.split(",")]
        notes = None

    try:
        duration = int(duration)
    except ValueError:
        print("\nError: Duration must be an integer representing minutes.")
        divider()
        menu()
        return

    data = Session(date=date, # type: ignore
                   duration=duration, 
                   focus=focus, 
                   notes=notes)
    result = create_session(data, None) # Error with no input for some reason, so it's set to None
    print(f"\n{result}")
    divider()
    menu()
    
def selection_view() -> None:
    """Handles the logic for viewing all sessions."""
    view_sessions()
    menu()

def selection_update() -> None:
    """Handles the logic for updating a session."""
    print("\nUpdate Session:"
          "\nTo update a session, you will need to provide the date of the session you want to update and the aspect you want to change (date, duration, focus, notes)."
          "\nExample input for aspect: date"
          "\nExample input for new value: 2023-09-16")

    # Display all sessions before updating
    view_sessions()

    # Update the sessions
    date = input("Enter the date of the session you want to update (YYYY-MM-DD): ")
    session_aspect = input("Enter the aspect you want to update (date, duration, focus, notes): ")
    edit = input(f"Enter the new value for {session_aspect}: ")

    session = get_session_by_date(date, None)
    if session is None:
        print(f"\nNo session found for the date: {date}")
        divider()
        menu()
        return
    if session_aspect == "date":
        session.date = edit
    elif session_aspect == "duration":
        try:
            session.duration = int(edit)
        except ValueError:
            print("\nError: Duration must be an integer representing minutes.")
            divider()
            menu()
            return
    elif session_aspect == "focus": 
        session.focus = edit
    elif session_aspect == "notes":
        session.notes = edit
    else:
        print("\nError: Invalid session aspect.")
        divider()
        menu()
        return

    result = update_session(session, None)
    print(f"\n{result}")
    divider()
    menu()

def selection_delete() -> None:
    """Handles the logic for deleting a session."""
    print("\nDelete Session:")
    print("To delete a session, you will need to provide the date of the session you want to delete.")
    print("Example input: 2023-09-15")
    divider()

    # Display all sessions before deletion
    sessions = read_sessions(None) # Error with no input for some reason, so it's set to None
    print("\nSessions:")
    for session in sessions:
        print(f"Date: {session[1]}, Duration: {session[2]} minutes, Focus: {session[3]}, Notes: {session[4]}")
    divider()

    # Delete the session
    date = input("Enter the date of the session you want to delete (YYYY-MM-DD): ")

    print(f"\nSessions on {date}:")

    session = get_session_by_date(date, None)
    if session:
        print(f"[{session.id}] Duration: {session.duration} minutes, Focus: {session.focus}, Notes: {session.notes}")
    else:
        print(f"No session found for the date: {date}")
        divider()
        menu()
        return
    try:
        id = int(input("Enter the ID of the session you want to delete: "))
    except ValueError:
        print("\nError: ID must be an integer.")
        divider()
        menu()
        return
    
    correct_id = id == session.id
    if not correct_id:
        print(f"\nError: No session found with ID: {id} for the date: {date}")
        divider()
        menu()
        return
    
    # Just in case
    y_n = input(f"Are you sure you want to delete this session on {date} with id [{id}]? (y/n): ")
    if y_n.lower() != "y":
        print("\nSession deletion cancelled.")
        divider()
        menu()
        return
    
    result = delete_session(id, None)
    print(f"\n{result}")
    divider()
    menu()

def handle_user_selection() -> None:
    """Handles the user's menu selection.
    """
    valid_selection = False
    while valid_selection != True:
        try:
            selection = int(input("Enter your selection (1-5): "))
        except ValueError:
            print("\nInvalid input. Please enter a number between 1 and 5.\n")
            continue

        if selection == 1:
            selection_add()
        elif selection == 2:
            selection_view()
        elif selection == 3:
            selection_update() 
        elif selection == 4:
            selection_delete()
        elif selection == 5: # Selection 5 is to exit the program.
            print("\nExiting the program. Goodbye!")
            divider()
            quit()
        else:
            print("\nInvalid selection.\n")

def main() -> None:
    """Runs the program."""
    create_db()
    greet()
    menu()
    handle_user_selection()

if __name__ == "__main__":
    main()