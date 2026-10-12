from collections import Counter
from .tickets import Ticket

STATUSES = ("open", "in_progress", "resolved")
PRIORITIES = ("critical", "high", "medium", "low")

def build_report(tickets: list[Ticket]) -> dict[str, dict[str, int]]:
    status_counts = Counter(ticket.status for ticket in tickets)
    priority_counts = Counter(ticket.priority for ticket in tickets)
    return {
        "by_status": {status: status_counts.get(status, 0) for status in STATUSES},
        "by_priority": {priority: priority_counts.get(priority, 0) for priority in PRIORITIES},
        "total": {"tickets": len(tickets)},
    }
