import unittest
from campusflow.tickets import calculate_priority, create_ticket

class TicketTests(unittest.TestCase):
    def test_priority_critical(self):
        self.assertEqual(calculate_priority("high", 10), "critical")
    def test_priority_high_for_high_urgency(self):
        self.assertEqual(calculate_priority("high", 2), "high")
    def test_priority_high_for_ten_users(self):
        self.assertEqual(calculate_priority("low", 10), "high")
    def test_priority_medium_for_medium_urgency(self):
        self.assertEqual(calculate_priority("medium", 1), "medium")
    def test_priority_medium_for_three_users(self):
        self.assertEqual(calculate_priority("low", 3), "medium")
    def test_priority_low(self):
        self.assertEqual(calculate_priority("low", 1), "low")
    def test_blank_title_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket("T001", "   ", "Network", "low", 1)
    def test_bad_category_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket("T001", "Wi-Fi down", "Internet", "low", 1)
    def test_zero_users_rejected(self):
        with self.assertRaises(ValueError):
            calculate_priority("low", 0)
    def test_title_is_trimmed(self):
        ticket = create_ticket("T001", "  Wi-Fi down  ", "Network", "low", 1)
        self.assertEqual(ticket.title, "Wi-Fi down")

if __name__ == "__main__":
    unittest.main()
