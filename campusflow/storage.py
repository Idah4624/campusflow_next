import json
from pathlib import Path
from .tickets import Ticket, validate_ticket

DEFAULT_FILE = Path("tickets.json")

def validate_collection(tickets: list[Ticket]) -> list[Ticket]:
    if not isinstance(tickets, list):
        raise ValueError("The JSON root must be a list of tickets.")
    seen = set()
    for ticket in tickets:
        validate_ticket(ticket)
        if ticket.id in seen:
            raise ValueError(f"Duplicate ticket ID: {ticket.id}.")
        seen.add(ticket.id)
    return tickets

def load_tickets(path: str | Path = DEFAULT_FILE) -> list[Ticket]:
    file_path = Path(path)
    if not file_path.exists():
        return []
    try:
        raw = json.loads(file_path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            raise ValueError("The JSON root must be a list of tickets.")
        tickets = [Ticket.from_dict(item) for item in raw]
        validate_collection(tickets)
        return tickets
    except (json.JSONDecodeError, TypeError, KeyError, ValueError) as exc:
        raise ValueError(f"Could not read ticket data from {file_path}: {exc}") from exc

def save_tickets(tickets: list[Ticket], path: str | Path = DEFAULT_FILE) -> None:
    validate_collection(tickets)
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps([ticket.to_dict() for ticket in tickets], indent=2), encoding="utf-8")

def next_ticket_id(tickets: list[Ticket]) -> str:
    highest = max((int(t.id[1:]) for t in tickets), default=0)
    return f"T{highest + 1:03d}"
