from dataclasses import dataclass, asdict
from typing import Any

CATEGORIES = {"Network", "Hardware", "Software", "Other"}
URGENCIES = {"low", "medium", "high"}

def calculate_priority(urgency: str, affected_users: int) -> str:
    """Calculate ticket priority using the project guide's ordered rules."""
    urgency = urgency.lower()
    if urgency not in URGENCIES:
        raise ValueError("Urgency must be low, medium, or high.")
    if not isinstance(affected_users, int) or isinstance(affected_users, bool) or affected_users < 1:
        raise ValueError("Affected users must be a positive integer.")

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

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Ticket":
        return cls(**data)

def create_ticket(ticket_id: str, title: str, category: str, urgency: str,
                  affected_users: int) -> Ticket:
    title = title.strip()
    if not title:
        raise ValueError("Title cannot be blank.")
    if category not in CATEGORIES:
        raise ValueError("Category must be Network, Hardware, Software, or Other.")
    urgency = urgency.lower()
    priority = calculate_priority(urgency, affected_users)
    return Ticket(
        id=ticket_id,
        title=title,
        category=category,
        urgency=urgency,
        affected_users=affected_users,
        priority=priority,
    )
