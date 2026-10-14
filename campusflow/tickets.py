from dataclasses import dataclass, field, asdict
from typing import Any
import re

CATEGORIES = {"Network", "Hardware", "Software", "Other"}
URGENCIES = {"low", "medium", "high"}
STATUSES = {"open", "in_progress", "resolved"}
PRIORITIES = {"critical", "high", "medium", "low"}

def validate_ticket_id(ticket_id: str) -> str:
    if not isinstance(ticket_id, str) or not re.fullmatch(r"T[0-9]{3,}", ticket_id):
        raise ValueError("Ticket ID must look like T001.")
    return ticket_id

def calculate_priority(urgency: str, affected_users: int) -> str:
    if not isinstance(urgency, str) or urgency.strip().lower() not in URGENCIES:
        raise ValueError("Urgency must be low, medium, or high.")
    if type(affected_users) is not int or affected_users <= 0:
        raise ValueError("Affected users must be a strictly positive integer.")
    urgency = urgency.strip().lower()
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"

@dataclass
class Ticket:
    id: str
    title: str
    category: str
    urgency: str
    affected_users: int
    priority: str
    status: str = "open"
    assigned_to: str | None = None
    notes: list[dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Ticket":
        if not isinstance(data, dict):
            raise ValueError("Each ticket must be a JSON object.")
        required = {"id", "title", "category", "urgency", "affected_users", "priority", "status", "assigned_to"}
        allowed = required | {"notes"}
        missing = required - data.keys()
        extra = data.keys() - allowed
        if missing:
            raise ValueError(f"Ticket is missing required fields: {', '.join(sorted(missing))}.")
        if extra:
            raise ValueError(f"Ticket has unknown fields: {', '.join(sorted(extra))}.")
        ticket = cls(**{**data, "notes": data.get("notes", [])})
        validate_ticket(ticket)
        return ticket

def validate_ticket(ticket: Ticket) -> None:
    validate_ticket_id(ticket.id)
    if not isinstance(ticket.title, str) or not ticket.title.strip():
        raise ValueError("Title cannot be blank.")
    if ticket.category not in CATEGORIES:
        raise ValueError("Category must be Network, Hardware, Software, or Other.")
    expected = calculate_priority(ticket.urgency, ticket.affected_users)
    if ticket.priority != expected:
        raise ValueError("Ticket priority does not match urgency and affected users.")
    if ticket.status not in STATUSES:
        raise ValueError("Status must be open, in_progress, or resolved.")
    if ticket.assigned_to is not None and (not isinstance(ticket.assigned_to, str) or not ticket.assigned_to.strip()):
        raise ValueError("Assignee must be a non-empty label or None.")
    if ticket.status == "in_progress" and not ticket.assigned_to:
        raise ValueError("An in_progress ticket must have an assignee.")
    if not isinstance(ticket.notes, list):
        raise ValueError("Ticket notes must be a list.")
    seen = set()
    for note in ticket.notes:
        if not isinstance(note, dict) or set(note) != {"note_id", "author", "message"}:
            raise ValueError("Each note must contain note_id, author, and message.")
        note_id, author, message = note["note_id"], note["author"], note["message"]
        if not isinstance(note_id, str) or not re.fullmatch(r"N[0-9]{3,}", note_id) or note_id in seen:
            raise ValueError("Note IDs must be valid and unique within a ticket.")
        if not isinstance(author, str) or not author.strip():
            raise ValueError("Note author cannot be blank.")
        if not isinstance(message, str) or not 5 <= len(message.strip()) <= 300:
            raise ValueError("Note message must be 5–300 characters after trimming.")
        seen.add(note_id)

def create_ticket(ticket_id: str, title: str, category: str, urgency: str, affected_users: int) -> Ticket:
    validate_ticket_id(ticket_id)
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title cannot be blank.")
    if not isinstance(category, str):
        raise ValueError("Choose a valid category.")
    category_map = {item.casefold(): item for item in CATEGORIES}
    canonical_category = category_map.get(category.strip().casefold())
    if not canonical_category:
        raise ValueError("Category must be Network, Hardware, Software, or Other.")
    urgency = urgency.strip().lower() if isinstance(urgency, str) else urgency
    priority = calculate_priority(urgency, affected_users)
    return Ticket(ticket_id, title.strip(), canonical_category, urgency, affected_users, priority)
