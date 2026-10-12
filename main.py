from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, change_status
from campusflow.queue import get_work_queue
from campusflow.reports import build_report
from campusflow.storage import load_tickets, save_tickets, next_ticket_id

def show_ticket(ticket):
    print(
        f"{ticket.id} | {ticket.title} | {ticket.category} | "
        f"{ticket.priority} | {ticket.status} | Assigned: {ticket.assigned_to or '-'}"
    )

def main():
    try:
        tickets = load_tickets()
    except ValueError as error:
        print(f"Storage error: {error}")
        return

    while True:
        print("\n====== CAMPUSFLOW HELPDESK ======")
        print("1. Create ticket")
        print("2. List tickets")
        print("3. Assign ticket")
        print("4. Change ticket status")
        print("5. View work queue")
        print("6. View report")
        print("7. Save and exit")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                title = input("Ticket title: ")
                category = input("Category (Network/Hardware/Software/Other): ").strip()
                urgency = input("Urgency (low/medium/high): ").strip()
                affected = int(input("Number of affected users: ").strip())
                ticket = create_ticket(next_ticket_id(tickets), title, category, urgency, affected)
                tickets.append(ticket)
                save_tickets(tickets)
                print(f"Created ticket {ticket.id} with {ticket.priority} priority.")
            elif choice == "2":
                if not tickets:
                    print("No tickets yet.")
                for ticket in tickets:
                    show_ticket(ticket)
            elif choice == "3":
                ticket_id = input("Ticket ID: ").strip().upper()
                ticket = next((t for t in tickets if t.id == ticket_id), None)
                if not ticket:
                    print("Ticket not found.")
                    continue
                assign_ticket(ticket, input("Assign to: "))
                save_tickets(tickets)
                print("Ticket assigned.")
            elif choice == "4":
                ticket_id = input("Ticket ID: ").strip().upper()
                ticket = next((t for t in tickets if t.id == ticket_id), None)
                if not ticket:
                    print("Ticket not found.")
                    continue
                new_status = input("New status (open/in_progress/resolved): ").strip()
                change_status(ticket, new_status)
                save_tickets(tickets)
                print("Ticket status updated.")
            elif choice == "5":
                queue = get_work_queue(tickets)
                if not queue:
                    print("No unresolved tickets.")
                for ticket in queue:
                    show_ticket(ticket)
            elif choice == "6":
                report = build_report(tickets)
                print("By status:", report["by_status"])
                print("By priority:", report["by_priority"])
                print("Total:", report["total"]["tickets"])
            elif choice == "7":
                save_tickets(tickets)
                print("Saved. Goodbye!")
                break
            else:
                print("Please choose a number from 1 to 7.")
        except (ValueError, TypeError) as error:
            print(f"Error: {error}")

if __name__ == "__main__":
    main()
