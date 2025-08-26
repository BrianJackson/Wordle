# tests/test_solver.py
import unittest
from solver import calculate_entropy, filter_candidates
from feedback import update_constraints

class TestSolver(unittest.TestCase):
    def test_entropy(self):
        words = ["apple", "angle", "alien", "amber", "annex"]
        entropy = calculate_entropy("apple", words)
        self.assertTrue(entropy > 0)

    def test_filtering(self):
        from collections import defaultdict
        words = ["crane", "slate", "stale", "tales", "least"]
        greens = {}
        yellows = defaultdict(set)
        grays = set()
        update_constraints("crane", "BBGBG", greens, yellows, grays)
        filtered = filter_candidates(words, "crane", "BBGBG", greens, yellows, grays)
        # Words that match: have 'a' in position 2 and 'e' in position 4, don't contain c,r,n
        self.assertIn("slate", filtered)
        self.assertNotIn("crane", filtered)  # crane contains c,r,n which are grays

if __name__ == "__main__":
    unittest.main()