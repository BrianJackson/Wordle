# solver.py
import math
import numpy as np
from functools import lru_cache
from feedback import get_feedback, matches_feedback, enforce_hard_mode
from wordlist import get_frequency

@lru_cache(maxsize=1024)
def cached_feedback(guess, solution):
    return get_feedback(guess, solution)

def calculate_entropy(guess, possible_solutions):
    patterns = [cached_feedback(guess, sol) for sol in possible_solutions]
    unique, counts = np.unique(patterns, return_counts=True)
    probs = counts / len(possible_solutions)
    entropy = -np.sum(probs * np.log2(probs))
    return float(entropy)

def rank_suggestions(candidates, greens, yellows, grays):
    # Single pass constraint check; avoids duplicated gray filtering logic
    valid = [w for w in candidates if enforce_hard_mode(w, greens, yellows, grays)]
    scored = []
    for word in valid:
        entropy = calculate_entropy(word, valid)
        frequency = get_frequency(word)
        score = entropy * frequency
        scored.append((word, score, entropy, frequency))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:5]

def filter_candidates(candidates, guess, feedback, greens, yellows, grays):
    return [
        word for word in candidates
        if matches_feedback(guess, word, feedback)
        and enforce_hard_mode(word, greens, yellows, grays)
    ]