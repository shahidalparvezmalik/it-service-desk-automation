import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from classifier import classify_ticket
from priority_engine import recommend_priority
from workflow import analyze_ticket


class WorkflowTests(unittest.TestCase):
    def test_classification(self):
        result = classify_ticket("User cannot access the shared folder due to a permission issue.")
        self.assertEqual(result.category, "Access Management")
        self.assertGreaterEqual(result.confidence, 0.75)

    def test_priority(self):
        result = recommend_priority("High", "Medium")
        self.assertEqual(result.priority, "P2")

    def test_high_risk_requires_approval(self):
        result = analyze_ticket(
            "Application server is unavailable",
            impact="High",
            urgency="High",
            action="production change",
        )
        self.assertEqual(result["priority"], "P1")
        self.assertTrue(result["human_approval_required"])
        self.assertFalse(result["automation_eligible"])

    def test_safe_action_can_be_eligible(self):
        result = analyze_ticket(
            "My account is locked after several failed attempts.",
            impact="Low",
            urgency="Low",
            action="account unlock",
        )
        self.assertEqual(result["category"], "Access Management")
        self.assertFalse(result["human_approval_required"])
        self.assertTrue(result["automation_eligible"])


if __name__ == "__main__":
    unittest.main()
