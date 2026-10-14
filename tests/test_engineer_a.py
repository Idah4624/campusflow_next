import json, tempfile, unittest
from pathlib import Path
from campusflow.tickets import create_ticket, calculate_priority, Ticket
from campusflow.workflow import assign_ticket, change_status, add_note, view_notes
from campusflow.storage import load_tickets, save_tickets, next_ticket_id

class EngineerATests(unittest.TestCase):
    def ticket(self, ticket_id="T001", users=1):
        return create_ticket(ticket_id, "WiFi router issue", "Network", "low", users)

    def test_priority_precedence(self):
        self.assertEqual(calculate_priority("high", 10), "critical")
        self.assertEqual(calculate_priority("high", 2), "high")
        self.assertEqual(calculate_priority("low", 10), "high")
        self.assertEqual(calculate_priority("medium", 1), "medium")
        self.assertEqual(calculate_priority("low", 3), "medium")

    def test_invalid_user_counts(self):
        for value in (0, -1, 1.5, True, "2"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                calculate_priority("low", value)

    def test_blank_title_and_invalid_category_rejected(self):
        with self.assertRaises(ValueError): create_ticket("T001", "  ", "Network", "low", 1)
        with self.assertRaises(ValueError): create_ticket("T001", "Title", "Internet", "low", 1)

    def test_unassigned_ticket_cannot_start_and_is_unchanged(self):
        t = self.ticket(); before = t.to_dict()
        with self.assertRaises(ValueError): change_status(t, "in_progress")
        self.assertEqual(t.to_dict(), before)

    def test_resolved_ticket_cannot_be_assigned(self):
        t = self.ticket(); change_status(t, "resolved"); before = t.to_dict()
        with self.assertRaises(ValueError): assign_ticket(t, "Sam")
        self.assertEqual(t.to_dict(), before)

    def test_note_id_and_validation(self):
        t = self.ticket()
        with self.assertRaises(ValueError): add_note(t, "Mentor", "no")
        note = add_note(t, "Mentor A", "Router reboot attempted")
        self.assertEqual(note["note_id"], "N001")

    def test_resolved_note_requires_reopen(self):
        t = self.ticket(); add_note(t, "A", "First follow-up")
        change_status(t, "resolved")
        with self.assertRaises(ValueError): add_note(t, "B", "Second follow-up")
        change_status(t, "open")
        self.assertEqual(add_note(t, "B", "Second follow-up")["note_id"], "N002")

    def test_save_load_preserves_notes_and_ids(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "tickets.json"; t = self.ticket()
            add_note(t, "Mentor", "Router reboot attempted")
            save_tickets([t], path); loaded = load_tickets(path)
            self.assertEqual(loaded[0].notes, t.notes)
            self.assertEqual(add_note(loaded[0], "Mentor", "Switch ports checked")["note_id"], "N002")
            self.assertEqual(next_ticket_id(loaded), "T002")

    def test_duplicate_ids_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "tickets.json"; t = self.ticket()
            path.write_text(json.dumps([t.to_dict(), t.to_dict()]), encoding="utf-8")
            with self.assertRaises(ValueError): load_tickets(path)

    def test_corrupt_json_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "tickets.json"; path.write_text("{bad", encoding="utf-8")
            with self.assertRaises(ValueError): load_tickets(path)

if __name__ == "__main__": unittest.main()
