# solver.py
import math
from feedback import get_feedback, matches_feedback, enforce_hard_mode
from wordlist import get_frequency

def calculate_entropy(guess, possible_solutions):
    patterns = [get_feedback(guess, sol) for sol in possible_solutions]
    total = len(possible_solutions)
    counts = {}
    for pattern in patterns:
        counts[pattern] = counts.get(pattern, 0) + 1
    return -sum((count / total) * math.log2(count / total) for count in counts.values())

def rank_suggestions(candidates, greens, yellows, grays):
    scored = []
    for word in candidates:
        if not enforce_hard_mode(word, greens, yellows, grays):
            continue
        entropy = calculate_entropy(word, candidates)
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