import unittest
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, change_status
from campusflow.search import search_tickets, sort_search_results
from campusflow.reports import build_report
from campusflow.queue import get_work_queue
from campusflow.understanding_check import QUESTIONS, score_answers

class EngineerBTests(unittest.TestCase):
    def ticket(self, ticket_id="T001", title="WiFi router issue", category="Network", urgency="low", users=1):
        return create_ticket(ticket_id, title, category, urgency, users)

    def test_search_case_insensitive_substring(self):
        t = self.ticket()
        self.assertEqual(search_tickets([t], "WIFI"), [t])
        self.assertEqual(search_tickets([t], "router"), [t])

    def test_combined_filters_use_and(self):
        a = self.ticket("T001", "WiFi down", "Network", "low", 1)
        b = self.ticket("T002", "WiFi down", "Hardware", "low", 1)
        c = self.ticket("T003", "WiFi down", "Network", "high", 1)
        self.assertEqual(search_tickets([a, b, c], "wifi", "Network", "open", "low"), [a])

    def test_search_does_not_mutate_ticket(self):
        t = self.ticket(); before = t.to_dict(); search_tickets([t], "wifi")
        self.assertEqual(t.to_dict(), before)

    def test_empty_report_is_safe(self):
        report = build_report([])
        self.assertEqual(report["resolution_percentage"], 0.0)
        self.assertEqual(report["unresolved"], 0)

    def test_report_counts_statuses(self):
        a = self.ticket(); b = self.ticket("T002", "Laptop broken", "Hardware")
        assign_ticket(b, "Alex"); change_status(b, "in_progress")
        change_status(a, "resolved"); change_status(a, "open")
        report = build_report([a, b])
        self.assertEqual(report["by_status"]["open"], 1)
        self.assertEqual(report["by_status"]["in_progress"], 1)
        self.assertEqual(report["resolved"], 0); self.assertEqual(report["unresolved"], 2)

    def test_queue_only_open_and_numeric_id_tie_break(self):
        t10 = self.ticket("T010", "Issue ten"); t2 = self.ticket("T002", "Issue two")
        working = self.ticket("T003", "Working"); assign_ticket(working, "Alex"); change_status(working, "in_progress")
        self.assertEqual(get_work_queue([t10, working, t2]), [t2, t10])

    def test_quiz_scoring(self):
        correct = [q[2] for q in QUESTIONS]
        self.assertEqual(score_answers(correct), 6)

    def test_priority_sorting(self):
        low = self.ticket("T001", "Low")
        high = self.ticket("T002", "High", urgency="high")
        self.assertEqual(sort_search_results([low, high]), [high, low])

if __name__ == "__main__": unittest.main()
