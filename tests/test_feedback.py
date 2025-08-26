# tests/test_feedback.py
import unittest
from feedback import get_feedback, update_constraints

class TestFeedback(unittest.TestCase):
    def test_feedback_basic(self):
        self.assertEqual(get_feedback("crane", "slate"), "BBGBG")
        self.assertEqual(get_feedback("apple", "apple"), "GGGGG")
        self.assertEqual(get_feedback("apple", "allee"), "GBBYG")

    def test_update_constraints(self):
        from collections import defaultdict
        greens = {}
        yellows = defaultdict(set)
        grays = set()
        update_constraints("crane", "BBGBG", greens, yellows, grays)
        self.assertEqual(greens[2], 'a')
        self.assertIn('c', grays)
        self.assertIn('r', grays)
        self.assertIn('n', grays)

if __name__ == "__main__":
    unittest.main()