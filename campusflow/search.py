from .tickets import Ticket, CATEGORIES, STATUSES, PRIORITIES
def search_tickets(tickets: list[Ticket], title: str = "", category: str = "",
                   status: str = "", priority: str = "") -> list[Ticket]:
    """Read-only title substring search; every supplied filter must match."""
    title_term = title.strip().casefold()
    if category and category not in CATEGORIES:
        raise ValueError("Invalid category filter.")
    if status and status not in STATUSES:
        raise ValueError("Invalid status filter.")
    if priority and priority not in PRIORITIES:
        raise ValueError("Invalid priority filter.")
    return [t for t in tickets
            if title_term in t.title.casefold()
            and (not category or t.category == category)
            and (not status or t.status == status)
            and (not priority or t.priority == priority)]
def sort_search_results(tickets: list[Ticket]) -> list[Ticket]:
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return sorted(tickets, key=lambda t: (order[t.priority], int(t.id[1:])))
