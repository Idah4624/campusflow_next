import unittest
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, change_status
from campusflow.queue import get_work_queue
from campusflow.reports import build_report

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.ticket = create_ticket("T001", "Printer broken", "Hardware", "low", 1)

    def test_assign_ticket(self):
        assign_ticket(self.ticket, "Alex")
        self.assertEqual(self.ticket.assigned_to, "Alex")

    def test_cannot_start_unassigned_ticket(self):
        with self.assertRaises(ValueError):
            change_status(self.ticket, "in_progress")

    def test_can_start_after_assignment(self):
        assign_ticket(self.ticket, "Alex")
        change_status(self.ticket, "in_progress")
        self.assertEqual(self.ticket.status, "in_progress")

    def test_resolved_ticket_must_be_reopened(self):
        assign_ticket(self.ticket, "Alex")
        change_status(self.ticket, "in_progress")
        change_status(self.ticket, "resolved")
        with self.assertRaises(ValueError):
            change_status(self.ticket, "in_progress")

    def test_reopen_resolved_ticket(self):
        assign_ticket(self.ticket, "Alex")
        change_status(self.ticket, "in_progress")
        change_status(self.ticket, "resolved")
        change_status(self.ticket, "open")
        self.assertEqual(self.ticket.status, "open")

    def test_queue_excludes_resolved(self):
        other = create_ticket("T002", "Network outage", "Network", "high", 12)
        change_status(other, "resolved")
        self.assertEqual(get_work_queue([self.ticket, other]), [self.ticket])

    def test_queue_prioritizes_critical(self):
        critical = create_ticket("T002", "Network outage", "Network", "high", 12)
        self.assertEqual(get_work_queue([self.ticket, critical])[0], critical)

    def test_report_includes_zero_counts(self):
        report = build_report([self.ticket])
        self.assertEqual(report["by_status"]["resolved"], 0)
        self.assertEqual(report["by_priority"]["critical"], 0)

if __name__ == "__main__":
    unittest.main()
