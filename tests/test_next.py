import json, tempfile, unittest
from pathlib import Path
from campusflow.tickets import create_ticket, calculate_priority
from campusflow.workflow import assign_ticket, change_status, add_note, view_notes
from campusflow.storage import load_tickets, save_tickets, next_ticket_id
from campusflow.search import search_tickets, sort_search_results
from campusflow.reports import build_report
from campusflow.queue import get_work_queue
from campusflow.understanding_check import score_answers, QUESTIONS

class CampusFlowNextTests(unittest.TestCase):
    def ticket(self, id="T001", title="WiFi router issue", category="Network", urgency="low", users=1):
        return create_ticket(id, title, category, urgency, users)

    def test_priority_rule_precedence(self):
        self.assertEqual(calculate_priority("high", 10), "critical")
        self.assertEqual(calculate_priority("high", 2), "high")
        self.assertEqual(calculate_priority("low", 10), "high")
        self.assertEqual(calculate_priority("medium", 1), "medium")
        self.assertEqual(calculate_priority("low", 3), "medium")

    def test_unassigned_transition_preserves_ticket(self):
        t = self.ticket(); before = t.to_dict()
        with self.assertRaises(ValueError): change_status(t, "in_progress")
        self.assertEqual(t.to_dict(), before)

    def test_resolved_assignment_preserves_ticket(self):
        t = self.ticket(); change_status(t, "resolved"); before = t.to_dict()
        with self.assertRaises(ValueError): assign_ticket(t, "Sam")
        self.assertEqual(t.to_dict(), before)

    def test_invalid_affected_users(self):
        for value in (0, -1, 1.5, True, "2"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                calculate_priority("low", value)

    def test_invalid_category(self):
        with self.assertRaises(ValueError): self.ticket(category="Internet")

    def test_valid_note_id(self):
        t = self.ticket(); note = add_note(t, "Mentor A", "Router reboot attempted")
        self.assertEqual(note["note_id"], "N001")

    def test_invalid_note_does_not_consume_id(self):
        t = self.ticket()
        with self.assertRaises(ValueError): add_note(t, "Mentor", "no")
        self.assertEqual(add_note(t, "Mentor", "A valid note").get("note_id"), "N001")

    def test_resolved_note_rejected_and_reopen_allowed(self):
        t = self.ticket(); add_note(t, "A", "First follow-up")
        change_status(t, "resolved")
        with self.assertRaises(ValueError): add_note(t, "B", "Second follow-up")
        change_status(t, "open")
        self.assertEqual(add_note(t, "B", "Second follow-up")["note_id"], "N002")

    def test_case_insensitive_substring_search(self):
        t = self.ticket()
        self.assertEqual(search_tickets([t], "WIFI"), [t])
        self.assertEqual(search_tickets([t], "router"), [t])

    def test_combined_filters_are_and(self):
        a = self.ticket("T001", "WiFi down", "Network", "low", 1)
        b = self.ticket("T002", "WiFi down", "Hardware", "low", 1)
        c = self.ticket("T003", "WiFi down", "Network", "high", 1)
        self.assertEqual(search_tickets([a,b,c], "wifi", "Network", "open", "low"), [a])

    def test_search_does_not_mutate(self):
        t = self.ticket(); before = t.to_dict()
        search_tickets([t], "wifi")
        self.assertEqual(t.to_dict(), before)

    def test_empty_report(self):
        report = build_report([])
        self.assertEqual(report["resolution_percentage"], 0.0)
        self.assertEqual(report["unresolved"], 0)

    def test_report_counts_current_status(self):
        a = self.ticket(); b = self.ticket("T002", "Laptop broken", "Hardware", "low", 1)
        assign_ticket(b, "Alex"); change_status(b, "in_progress")
        change_status(a, "resolved"); change_status(a, "open")
        report = build_report([a,b])
        self.assertEqual(report["by_status"]["open"], 1)
        self.assertEqual(report["by_status"]["in_progress"], 1)
        self.assertEqual(report["resolved"], 0)
        self.assertEqual(report["unresolved"], 2)

    def test_save_load_notes_and_next_ids(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"tickets.json"; t = self.ticket()
            add_note(t, "Mentor", "Router reboot attempted")
            save_tickets([t], p); loaded = load_tickets(p)
            self.assertEqual(loaded[0].notes, t.notes)
            self.assertEqual(add_note(loaded[0], "Mentor", "Switch ports checked")["note_id"], "N002")
            self.assertEqual(next_ticket_id(loaded), "T002")

    def test_duplicate_ids_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"tickets.json"; t = self.ticket()
            p.write_text(json.dumps([t.to_dict(), t.to_dict()]), encoding="utf-8")
            with self.assertRaises(ValueError): load_tickets(p)

    def test_corrupt_json_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"tickets.json"; p.write_text("{bad", encoding="utf-8")
            with self.assertRaises(ValueError): load_tickets(p)

    def test_invalid_note_shape_rejected(self):
        t = self.ticket().to_dict(); t["notes"] = [{"note_id":"N001","author":"A","message":"valid note"}, {"note_id":"N001","author":"B","message":"another valid note"}]
        with self.assertRaises(ValueError):
            from campusflow.tickets import Ticket
            Ticket.from_dict(t)

    def test_queue_open_only_and_numeric_tie_break(self):
        t10 = self.ticket("T010", "Issue ten", "Network", "low", 1)
        t2 = self.ticket("T002", "Issue two", "Network", "low", 1)
        inprog = self.ticket("T003", "Working", "Network", "low", 1)
        assign_ticket(inprog, "Alex"); change_status(inprog, "in_progress")
        self.assertEqual(get_work_queue([t10, inprog, t2]), [t2, t10])

    def test_quiz_scoring(self):
        correct = [q[2] for q in QUESTIONS]
        self.assertEqual(score_answers(correct), 6)
        self.assertEqual(score_answers(["A"]*6), sum(1 for q in QUESTIONS if q[2] == "A"))

    def test_next_ticket_id_after_high_number(self):
        self.assertEqual(next_ticket_id([self.ticket("T012")]), "T013")

if __name__ == "__main__":
    unittest.main()
