# Introduction
Welcome to the CONTRIBUTING file! Here, any info you might need to contribute and help in this project's upbringing is right here. This file is primarily for a style guide.

## Table of Contents
1. [Introduction](#introduction)
2. [Standards](#code-standards-and-best-practices)
3. [Input & Validation](#user-input-validation)
4. [Function Design](#function-design)
5. [Logic & Structure](#logic-&-structure)
6. [Testing](#testing)
7. [Commit Messages](#commit-messages)

## Code Standards and Best Practices
- Follow existing patterns in the codebase unless intentionally refactoring
- Avoid duplicating logic
- Use simple, readable solutions
- Raise clear, descriptive exceptions when errors occur
- Separate concerns by layers (UI, Service, Database)
- If you modify code, leave it cleaner than you found it
- Do not optimize performance unless needed
- Imports at the top of the file and grouped by standard library, third-party, and local imports
- Docsting at the top of the file
- Comments explain why, not what
- Do not mix responsibilities between layers (ex. don't have database code in the service layer)
- Avoid using global variables, use constants or configuration files instead

## User Input Validation
- All user input must be thoroughly validated before entering the system.
- NEVER trust user input without validation
- Structured data must be represented using data classes or similar constructs to ensure type safety and clarity. 
- Collect it carefully, never assuming anything (ex. using int(), assuming they typed a number)

## Function Design
- All functions must include type hints and return values
- Functions should return consistent types 
- Use Optional[type] for functions that can return None
- Functions should not secretly modify unrelated data
- Functions should include Docstrings
- Functions should not exceed ~25 lines, else, split it. Don't split if it's clearly one task.

## Logic & Structure
- Avoid hardcoding logic that has meaning ex.
```bash
DO NOT:
if duration > 60...

DO:
MAX_SESSION_DURATION = 60

if duration > MAX_SESSION_DURATION...
```
- Make meaningful variable names
- Avoid repetitive code, if you find yourself copy-pasting, consider refactoring into a function or loop
- Make it clean and readable; don't be afraid of blank lines

## Testing
- Write tests as you write the functions
- DO NOT wait until the end to write tests
- Utilize fixtures
- Make sure you are asserting important info, not something like a "success" message
- Never test in the main database. Always create a test database that is auto-deleted.
- Don't be afraid to comment here. People need to understand your tests.

## Commit Messages
- Write commit messages that describe what changed and why.
- No commits over 2 sentences, if so, try separating commits.
- Commit after completing a logical unit of work, not after every line.
- Push after each commit, don't wait until the end to push.
- Be straight-to-the-point and concise
