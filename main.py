from campusflow.tickets import create_ticket, CATEGORIES, STATUSES, PRIORITIES
from campusflow.workflow import assign_ticket, change_status, add_note, view_notes
from campusflow.queue import get_work_queue
from campusflow.search import search_tickets, sort_search_results
from campusflow.reports import build_report
from campusflow.storage import load_tickets, save_tickets, next_ticket_id
from campusflow.understanding_check import QUESTIONS, score_answers

def show_ticket(ticket):
    print(f"{ticket.id} | {ticket.title} | {ticket.category} | {ticket.priority} | "
          f"{ticket.status} | Assigned: {ticket.assigned_to or '-'}")

def choose_filter(label, options):
    while True:
        value = input(f"{label} ({'/'.join(sorted(options))}, blank for any): ").strip()
        if not value:
            return ""
        canonical = {item.casefold(): item for item in options}.get(value.casefold())
        if canonical:
            return canonical
        print("Invalid option. Please try again.")

def search_view(tickets):
    term = input("Title contains (blank for any title): ")
    category = choose_filter("Category", CATEGORIES)
    status = choose_filter("Status", STATUSES)
    priority = choose_filter("Priority", PRIORITIES)
    results = search_tickets(tickets, term, category, status, priority)
    if input("Sort by priority then ticket ID? (y/N): ").strip().lower() == "y":
        results = sort_search_results(results)
    if not results:
        print("No matching tickets.")
    for ticket in results:
        show_ticket(ticket)

def understanding_check():
    answers = []
    explanations = []
    print("\n=== Engineering Understanding Check ===")
    for index, (question, options, correct) in enumerate(QUESTIONS, 1):
        print(f"\nQ{index}. {question}")
        for letter, option in zip("ABCD", options):
            print(f"  {letter}. {option}")
        while True:
            answer = input("Your answer (A/B/C/D): ").strip().upper()
            if answer in "ABCD" and len(answer) == 1:
                break
            print("Enter A, B, C, or D.")
        answers.append(answer)
        print("Correct." if answer == correct else f"Not quite. Correct answer: {correct}.")
        if index in (1, 4):
            explanations.append(input(f"Briefly explain your answer to Q{index}: ").strip())
    print(f"Final score: {score_answers(answers)}/6")
    learning_path = "docs/understanding-check-reflection.md"
    from pathlib import Path
    Path(learning_path).parent.mkdir(parents=True, exist_ok=True)
    with open(learning_path, "a", encoding="utf-8") as handle:
        handle.write("\n## Quiz attempt\n")
        handle.write(f"Score: {score_answers(answers)}/6\n")
        handle.write(f"Q1 explanation: {explanations[0]}\n")
        handle.write(f"Q4 explanation: {explanations[1]}\n")

def main():
    try:
        tickets = load_tickets()
    except ValueError as error:
        print(f"Storage error: {error}\nCurrent data was not loaded. Fix the JSON file and restart.")
        return
    while True:
        print("\n====== CAMPUSFLOW NEXT ======")
        for number, label in enumerate([
            "Create ticket", "List tickets", "Assign ticket", "Change ticket status",
            "View Open Work Queue", "View report", "Search tickets", "Add Follow-up Note",
            "View Ticket Notes", "Engineering Understanding Check", "Save and exit"
        ], 1):
            print(f"{number}. {label}")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                title = input("Ticket title: ")
                category = input("Category (Network/Hardware/Software/Other): ")
                urgency = input("Urgency (low/medium/high): ")
                affected = input("Number of affected users: ").strip()
                if not affected.isdecimal():
                    raise ValueError("Affected users must be a positive integer.")
                ticket = create_ticket(next_ticket_id(tickets), title, category, urgency, int(affected))
                tickets.append(ticket)
                save_tickets(tickets)
                print(f"Created {ticket.id} with {ticket.priority} priority.")
            elif choice == "2":
                print("No tickets yet." if not tickets else "")
                for ticket in tickets: show_ticket(ticket)
            elif choice in {"3", "4", "8", "9"}:
                ticket_id = input("Ticket ID: ").strip().upper()
                ticket = next((t for t in tickets if t.id == ticket_id), None)
                if ticket is None:
                    print("Ticket not found."); continue
                if choice == "3":
                    assign_ticket(ticket, input("Assign to: "))
                    save_tickets(tickets); print("Ticket assigned.")
                elif choice == "4":
                    change_status(ticket, input("New status (open/in_progress/resolved): ").strip())
                    save_tickets(tickets); print("Ticket status updated.")
                elif choice == "8":
                    note = add_note(ticket, input("Author label: "), input("Note (5–300 characters): "))
                    save_tickets(tickets); print(f"Added note {note['note_id']}.")
                else:
                    notes = view_notes(ticket)
                    if not notes: print("No notes for this ticket.")
                    for note in notes: print(f"{note['note_id']} | {note['author']} | {note['message']}")
            elif choice == "5":
                queue = get_work_queue(tickets)
                if not queue: print("No open tickets.")
                for ticket in queue: show_ticket(ticket)
            elif choice == "6":
                report = build_report(tickets)
                print(f"Total tickets: {report['total']['tickets']}")
                print("By status:", report["by_status"])
                print("By priority:", report["by_priority"])
                print("By category:", report["by_category"])
                print(f"Unresolved: {report['unresolved']}; Resolved: {report['resolved']}")
                print(f"Resolution: {report['resolution_percentage']}%")
            elif choice == "7":
                search_view(tickets)
            elif choice == "10":
                understanding_check()
            elif choice == "11":
                save_tickets(tickets); print("Saved. Goodbye!"); break
            else:
                print("Please choose a number from 1 to 11.")
        except (ValueError, TypeError) as error:
            print(f"Error: {error}")

if __name__ == "__main__":
    main()
