from .tickets import Ticket, STATUSES

def assign_ticket(ticket: Ticket, person: str) -> Ticket:
    if not isinstance(person, str) or not person.strip():
        raise ValueError("Assignee cannot be blank.")
    if ticket.status == "resolved":
        raise ValueError("Reopen a resolved ticket before assigning it.")
    ticket.assigned_to = person.strip()
    return ticket

def change_status(ticket: Ticket, new_status: str) -> Ticket:
    if not isinstance(new_status, str) or new_status not in STATUSES:
        raise ValueError("Status must be open, in_progress, or resolved.")
    if ticket.status == "resolved" and new_status != "open":
        raise ValueError("A resolved ticket must be explicitly reopened to open first.")
    if new_status == "in_progress" and not ticket.assigned_to:
        raise ValueError("Assign the ticket before moving it to in_progress.")
    ticket.status = new_status
    return ticket

def next_note_id(ticket: Ticket) -> str:
    highest = 0
    for note in ticket.notes:
        digits = "".join(ch for ch in note["note_id"] if ch.isdigit())
        if digits:
            highest = max(highest, int(digits))
    return f"N{highest + 1:03d}"

def add_note(ticket: Ticket, author: str, message: str) -> dict[str, str]:
    if ticket.status not in {"open", "in_progress"}:
        raise ValueError("Reopen the ticket before adding a note.")
    if not isinstance(author, str) or not author.strip():
        raise ValueError("Note author cannot be blank.")
    if not isinstance(message, str) or not 5 <= len(message.strip()) <= 300:
        raise ValueError("Note message must be 5–300 characters after trimming.")
    note = {"note_id": next_note_id(ticket), "author": author.strip(), "message": message.strip()}
    ticket.notes.append(note)
    return note

def view_notes(ticket: Ticket) -> list[dict[str, str]]:
    return sorted((dict(note) for note in ticket.notes), key=lambda n: int(n["note_id"][1:]))
