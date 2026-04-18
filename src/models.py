from dataclasses import dataclass
from datetime import date

@dataclass
class Session:
    date: date | str
    duration: int
    focus: str = "No Focus"
    notes: str | None = None
    id: int | None = None
    
    def __post_init__(self):
        if not isinstance(self.date, (date, str)):
            raise ValueError("Date must be a date object.")
        if not isinstance(self.duration, int):
            raise ValueError("Duration must be an integer.")
        if not isinstance(self.focus, str):
            raise ValueError("Focus must be a string.")
        if self.focus == "":
            self.focus = "No Focus"
        if self.notes is not None and not isinstance(self.notes, str):
            raise ValueError("Notes must be a string or None.")