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
        words = ["apple", "angle", "alien", "amber", "annex"]
        greens = {}
        yellows = {}
        grays = set()
        update_constraints("apple", "BYGBY", greens, yellows, grays)
        filtered = filter_candidates(words, "apple", "BYGBY", greens, yellows, grays)
        self.assertIn("angle", filtered)
        self.assertNotIn("apple", filtered)

if __name__ == "__main__":
    unittest.main()