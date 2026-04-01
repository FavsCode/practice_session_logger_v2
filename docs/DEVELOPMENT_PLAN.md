# Concept

An account-based session-logger to analyze logged session data for display of analytics.

# Scope

## DOES:

- Handle CRUD of session records

- Analyze and collect metrics on data

- Possess a login

- Store and save account data

## DOES NOT:

- Use an environment

- Have UI other than console UI

- Utilize packaging

- Use languages other than SQLite and Python

# Code Style Guide
In 
```bash
CONTIBUTING.md
```

# Main.py Style Guide
- divider() before every display execution
- A blank line before and after each divider
- Blank line between input requests
- Pretty much a blank line between everything (every different operation ex. menu & selection, header & displayed data, etc.)

# Session Data Model
```bash
Session: 

    ID: (PRIMARY KEY)	 

    Date: (Stored as TEXT in ISO format: YYYY-MM-DD) 

    Duration: (INTEGER as minutes) 

    Focus: (STRING, default = “No Focus”) 

    Notes: (TEXT, optional) 
```

# Account Data Model
```bash
Username:

    password:
```

# Program Flow 
```bash
Start program 

Show login:
    PRACTICE_SESSION_LOGGER V2

    Login
    username:
    password:

If valid input
Show menu: 

    1. Add session 

    2. View sessions 

    3. Update session 

    4. Delete session 

    5. Exit

If "5" selected

End program 
```
# File Structure 
```bash
practice_session_logger_v2/ 

    docs/
        CONTRIBUTING.md --> The project style guide for contributing
        DEVELOPMENT_LOG.md --> Logs of all significant changes according to plan
        DEVELOPMENT_PLAN.md --> The project blueprint and objectives
    
    src/
        __init__.py --> Initializes module
        database.py --> Operates on practice_sessions using info from the session model
        session.py --> Contains a session schema and imposes rules on main/user data
        
    tests/
        test_database.py --> Contains tests for interactions with the database
        test_session.py --> Contains tests for the CRUD operations related to database.py

    .gitignore --> Tells git to ignore the SQLite file

    main.py --> Entry point of the program

    practice_sessions.sqlite --> Stores all practice session data; made upon program startup 
    
    README.md --> Information on the program and how to run it

    
```

# Milestones 

1. Successful CRUD operations on practice_sessions 

2. Automated tests for CRUD operations

3. Data analytics functions exist and work

4. Automated test for data analytics

5. User system implemented

6. CLI menu interactions

7. Refactor + type hints cleanup

# Risk Notes 

- User-system inplementation could ruin data storage

- User system could mess with CLI

- Putting everything together might have tiny details that are ignored

