from .tickets import Ticket

PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}

def _numeric_id(ticket: Ticket) -> int:
    digits = "".join(ch for ch in ticket.id if ch.isdigit())
    return int(digits or 0)

def get_work_queue(tickets: list[Ticket]) -> list[Ticket]:
    unresolved = [ticket for ticket in tickets if ticket.status != "resolved"]
    return sorted(unresolved, key=lambda t: (PRIORITY_ORDER.get(t.priority, 99), _numeric_id(t)))
