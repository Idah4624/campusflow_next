# Design decisions

- Tickets are represented by a Python dataclass to keep the fields explicit.
- Priority is calculated once when a ticket is created, following the ordered rules in the project guide.
- Ticket IDs are sequential (`T001`, `T002`, ...), calculated from the largest existing numeric ID so reloads do not restart numbering.
- The JSON file stores a list of ticket objects. A missing file means a fresh project; malformed data raises a readable error.
- Workflow rules are kept in `workflow.py`, separate from ticket creation and validation.
- Queue sorting uses priority order, then the numeric part of the ticket ID.
