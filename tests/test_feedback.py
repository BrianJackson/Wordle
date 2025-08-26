# tests/test_feedback.py
import unittest
from feedback import get_feedback, update_constraints

class TestFeedback(unittest.TestCase):
    def test_feedback_basic(self):
        self.assertEqual(get_feedback("crane", "slate"), "BYGBY")
        self.assertEqual(get_feedback("apple", "apple"), "GGGGG")
        self.assertEqual(get_feedback("apple", "allee"), "GYBBG")

    def test_update_constraints(self):
        greens = {}
        yellows = {}
        grays = set()
        update_constraints("crane", "BYGBY", greens, yellows, grays)
        self.assertEqual(greens[2], 'a')
        self.assertIn('r', yellows)
        self.assertIn('e', yellows)
        self.assertIn('c', grays)
        self.assertIn('n', grays)

if __name__ == "__main__":
    unittest.main()