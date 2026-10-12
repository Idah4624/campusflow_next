from .tickets import Ticket

def assign_ticket(ticket: Ticket, person: str) -> Ticket:
    person = person.strip()
    if not person:
        raise ValueError("Assignee cannot be blank.")
    if ticket.status == "resolved":
        raise ValueError("Reopen a resolved ticket before assigning it.")
    ticket.assigned_to = person
    return ticket

def change_status(ticket: Ticket, new_status: str) -> Ticket:
    allowed = {"open", "in_progress", "resolved"}
    if new_status not in allowed:
        raise ValueError("Status must be open, in_progress, or resolved.")
    if ticket.status == "resolved" and new_status != "open":
        raise ValueError("A resolved ticket must be explicitly reopened to open first.")
    if new_status == "in_progress" and not ticket.assigned_to:
        raise ValueError("Assign the ticket before moving it to in_progress.")
    ticket.status = new_status
    return ticket
