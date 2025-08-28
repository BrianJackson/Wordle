# tests/test_feedback.py
import unittest
from feedback import get_feedback, update_constraints

class TestFeedback(unittest.TestCase):
    def test_feedback_basic(self):
        # crane vs slate
        self.assertEqual(get_feedback("crane", "slate"), "BBGBG")
        # identical
        self.assertEqual(get_feedback("apple", "apple"), "GGGGG")
        # apple vs allee
        self.assertEqual(get_feedback("apple", "allee"), "GBBYG")

    def test_update_constraints(self):
        greens = {}
        yellows = {}
        grays = set()
        pattern = get_feedback("crane", "slate")  # BBGBG
        update_constraints("crane", pattern, greens, yellows, grays)
        # Greens at positions 2 (a) and 4 (e)
        self.assertEqual(greens[2], 'a')
        self.assertEqual(greens[4], 'e')
        # Letters c, r, n should be gray
        for l in ['c', 'r', 'n']:
            self.assertIn(l, grays)
        # No yellows expected in this pattern
        self.assertEqual(len(yellows), 0)

    def test_repeated_letter_feedback(self):
        # Scenario 1: guess has two p's, solution has one (APPLE vs ALLEE)
        pattern1 = get_feedback("apple", "allee")  # Expected GBBYG
        self.assertEqual(pattern1, "GBBYG")
        greens = {}
        yellows = {}
        grays = set()
        update_constraints("apple", pattern1, greens, yellows, grays)
        self.assertEqual(greens[0], 'a')
        self.assertEqual(greens[4], 'e')
        self.assertIn('l', yellows)  # yellow letter tracked
        # Extra 'p' occurrences become gray
        self.assertIn('p', grays)
        # 'l' should not invalidate despite possibly also in grays set (depends on other cases)

        # Scenario 2: guess has two l's, solution has one (ALLEE vs APPLE)
        pattern2 = get_feedback("allee", "apple")  # Expected GYBBG
        self.assertEqual(pattern2, "GYBBG")
        greens2 = {}
        yellows2 = {}
        grays2 = set()
        update_constraints("allee", pattern2, greens2, yellows2, grays2)
        self.assertEqual(greens2[0], 'a')
        self.assertEqual(greens2[4], 'e')
        self.assertIn('l', yellows2)
        # Second 'l' marked gray shouldn't block due to yellows key presence
        # Ensure enforce_hard_mode logic condition holds: l can appear in candidate words

if __name__ == "__main__":
    unittest.main()