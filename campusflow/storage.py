import json
from pathlib import Path
from .tickets import Ticket

DEFAULT_FILE = Path("tickets.json")

def load_tickets(path: str | Path = DEFAULT_FILE) -> list[Ticket]:
    file_path = Path(path)
    if not file_path.exists():
        return []
    try:
        raw = json.loads(file_path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            raise ValueError("The JSON root must be a list of tickets.")
        return [Ticket.from_dict(item) for item in raw]
    except (json.JSONDecodeError, TypeError, KeyError) as exc:
        raise ValueError(f"Could not read ticket data from {file_path}: {exc}") from exc

def save_tickets(tickets: list[Ticket], path: str | Path = DEFAULT_FILE) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        json.dumps([ticket.to_dict() for ticket in tickets], indent=2),
        encoding="utf-8",
    )

def next_ticket_id(tickets: list[Ticket]) -> str:
    highest = 0
    for ticket in tickets:
        digits = "".join(ch for ch in ticket.id if ch.isdigit())
        if digits:
            highest = max(highest, int(digits))
    return f"T{highest + 1:03d}"
