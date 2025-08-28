# feedback.py
from collections import defaultdict

def get_feedback(guess, solution):
    feedback = ['B'] * 5
    solution_used = [False] * 5
    for i in range(5):
        if guess[i] == solution[i]:
            feedback[i] = 'G'
            solution_used[i] = True
    for i in range(5):
        if feedback[i] == 'G':
            continue
        for j in range(5):
            if not solution_used[j] and guess[i] == solution[j]:
                feedback[i] = 'Y'
                solution_used[j] = True
                break
    return ''.join(feedback)

def matches_feedback(guess, candidate, feedback):
    return get_feedback(guess, candidate) == feedback

def enforce_hard_mode(word, greens, yellows, grays):
    for i, g in greens.items():
        if word[i] != g:
            return False
    for letter, positions in yellows.items():
        if letter not in word:
            return False
        if any(word[pos] == letter for pos in positions):
            return False
    for letter in grays:
        if letter in word and letter not in greens.values() and letter not in yellows:
            return False
    return True

def update_constraints(guess, feedback, greens, yellows, grays):
    for i, fb in enumerate(feedback):
        letter = guess[i]
        if fb == 'G':
            greens[i] = letter
        elif fb == 'Y':
            if letter not in yellows:
                yellows[letter] = set()
            yellows[letter].add(i)
        elif fb == 'B':
            grays.add(letter)