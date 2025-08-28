# tests/test_solver.py
import unittest
from solver import calculate_entropy, filter_candidates, rank_suggestions
from feedback import update_constraints, enforce_hard_mode

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
        # Use actual pattern of apple vs angle
        pattern = get_feedback = __import__('feedback').get_feedback("apple", "angle")
        update_constraints("apple", pattern, greens, yellows, grays)
        filtered = filter_candidates(words, "apple", pattern, greens, yellows, grays)
        self.assertIn("angle", filtered)
        self.assertNotIn("apple", filtered)

    def test_rank_suggestions_respects_constraints(self):
        # Setup a small candidate pool
        candidates = ["crane", "slate", "clash", "crony", "trace"]
        greens = {}
        yellows = {}
        grays = set()
        # Derive pattern from actual solution slate
        pattern = __import__('feedback').get_feedback("crane", "slate")
        update_constraints("crane", pattern, greens, yellows, grays)
        # Ensure enforce_hard_mode filters correctly
        valid = [w for w in candidates if enforce_hard_mode(w, greens, yellows, grays)]
        suggestions = rank_suggestions(candidates, greens, yellows, grays)
        suggested_words = [w for w, *_ in suggestions]
        for w in suggested_words:
            self.assertIn(w, valid)
        # Suggestions limited to 5
        self.assertLessEqual(len(suggestions), 5)

    def test_empty_after_over_filter(self):
        candidates = ["apple", "angle"]
        greens = {0: 'z'}  # Impossible constraint
        yellows = {}
        grays = set(['a'])
        suggestions = rank_suggestions(candidates, greens, yellows, grays)
        self.assertEqual(suggestions, [])

if __name__ == "__main__":
    unittest.main()