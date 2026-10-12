import tempfile
import unittest
from pathlib import Path
from campusflow.tickets import create_ticket
from campusflow.storage import load_tickets, save_tickets, next_ticket_id

class StorageTests(unittest.TestCase):
    def test_missing_file_starts_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(load_tickets(Path(directory) / "missing.json"), [])

    def test_save_and_reload(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            original = create_ticket("T001", "Wi-Fi down", "Network", "high", 10)
            save_tickets([original], path)
            loaded = load_tickets(path)
            self.assertEqual(loaded[0].to_dict(), original.to_dict())

    def test_next_id_after_reload(self):
        tickets = [create_ticket("T003", "Screen broken", "Hardware", "low", 1)]
        self.assertEqual(next_ticket_id(tickets), "T004")

    def test_malformed_json_gives_clear_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text("{bad json", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_tickets(path)

if __name__ == "__main__":
    unittest.main()
