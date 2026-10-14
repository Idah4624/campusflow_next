from .tickets import Ticket
PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
def _numeric_id(ticket: Ticket) -> int:
    return int("".join(ch for ch in ticket.id if ch.isdigit()) or 0)
def get_work_queue(tickets: list[Ticket]) -> list[Ticket]:
    """Original queue: OPEN tickets only, priority then numeric ticket ID."""
    opened = [ticket for ticket in tickets if ticket.status == "open"]
    return sorted(opened, key=lambda t: (PRIORITY_ORDER[t.priority], _numeric_id(t)))
