from collections import Counter
from .tickets import Ticket, STATUSES, PRIORITIES, CATEGORIES
def build_report(tickets: list[Ticket]) -> dict:
    statuses = Counter(t.status for t in tickets)
    priorities = Counter(t.priority for t in tickets)
    categories = Counter(t.category for t in tickets)
    total = len(tickets)
    resolved = statuses.get("resolved", 0)
    return {
        "total": {"tickets": total},
        "by_status": {s: statuses.get(s, 0) for s in sorted(STATUSES)},
        "by_priority": {p: priorities.get(p, 0) for p in ("critical", "high", "medium", "low")},
        "by_category": {c: categories.get(c, 0) for c in sorted(CATEGORIES)},
        "unresolved": statuses.get("open", 0) + statuses.get("in_progress", 0),
        "resolved": resolved,
        "resolution_percentage": round(resolved / total * 100, 2) if total else 0.0,
    }
