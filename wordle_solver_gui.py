import tkinter as tk
from tkinter import messagebox
import os
import math
from collections import Counter
from wordfreq import word_frequency

# Load Wordle list
def load_wordle_list():
    path = os.path.join(os.path.dirname(__file__), 'wordle_list.txt')
    try:
        with open(path, 'r') as f:
            return [line.strip().lower() for line in f if len(line.strip()) == 5]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load word list: {e}")
        return []

# Wordle feedback logic
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

def calculate_entropy(guess, possible_solutions):
    patterns = [get_feedback(guess, sol) for sol in possible_solutions]
    counts = Counter(patterns)
    total = len(possible_solutions)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())

def get_frequency(word):
    return word_frequency(word, 'en') or 0.00001

def filter_words(words, guess, feedback):
    return [word for word in words if matches_feedback(guess, word, feedback)]

# Load data
wordle_list = load_wordle_list()
current_candidates = wordle_list.copy()

# GUI setup
root = tk.Tk()
root.title("Wordle Solver")

fb_display = {'G': '🟩', 'Y': '🟨', 'B': '⬜'}
tile_colors = {'G': '#6aaa64', 'Y': '#c9b458', 'B': '#787c7e'}
fb_state = ['B'] * 5
feedback_buttons = []

# Suggest next guess and show top 5
def suggest_next_guess():
    if not current_candidates:
        messagebox.showinfo("No Candidates", "No words left to suggest.")
        return

    scores = []
    for word in current_candidates:
        entropy = calculate_entropy(word, current_candidates)
        frequency = get_frequency(word)
        score = entropy * frequency
        scores.append((word, score, entropy, frequency))

    scores.sort(key=lambda x: x[1], reverse=True)
    top5 = scores[:5]

    best_guess.set(top5[0][0].upper())
    guess_log.insert(tk.END, f"Suggested: {top5[0][0].upper()} (Entropy: {top5[0][2]:.3f}, Frequency: {top5[0][3]:.6f})\n")

    top5_output.delete(1.0, tk.END)
    top5_output.insert(tk.END, "Top 5 Suggestions:\n")
    for word, score, entropy, freq in top5:
        top5_output.insert(tk.END, f"{word.upper():<8} Score: {score:.6f} | Entropy: {entropy:.3f} | Freq: {freq:.6f}\n")

    update_remaining_display()

# Apply feedback
def apply_feedback():
    guess = best_guess.get().lower()
    if len(guess) != 5:
        messagebox.showerror("Invalid Guess", "Guess must be 5 letters.")
        return
    feedback = ''.join([fb_state[i] for i in range(5)])
    global current_candidates
    current_candidates = filter_words(current_candidates, guess, feedback)
    guess_log.insert(tk.END, f"{guess.upper()} → {''.join([fb_display[fb_state[i]] for i in range(5)])}\n")
    best_guess.set("")
    for i in range(5):
        fb_state[i] = 'B'
        feedback_buttons[i].config(text=fb_display['B'], bg=tile_colors['B'])
    suggest_button.config(state="normal")
    update_remaining_display()

# Restart solver
def restart_solver():
    global current_candidates
    current_candidates = wordle_list.copy()
    best_guess.set("")
    guess_log.delete(1.0, tk.END)
    top5_output.delete(1.0, tk.END)
    remaining_output.delete(1.0, tk.END)
    for i in range(5):
        fb_state[i] = 'B'
        feedback_buttons[i].config(text=fb_display['B'], bg=tile_colors['B'])
    suggest_button.config(state="disabled")
    update_remaining_display()

# Cycle feedback button
def cycle_feedback(i):
    current = fb_state[i]
    next_state = {'B': 'Y', 'Y': 'G', 'G': 'B'}[current]
    fb_state[i] = next_state
    feedback_buttons[i].config(text=fb_display[next_state], bg=tile_colors[next_state])
    if any(f != 'B' for f in fb_state):
        suggest_button.config(state="normal")
    else:
        suggest_button.config(state="disabled")

# Display remaining candidates
def update_remaining_display():
    remaining_output.delete(1.0, tk.END)
    remaining_output.insert(tk.END, f"Remaining Candidates: {len(current_candidates)}\n")
    for word in current_candidates[:20]:
        remaining_output.insert(tk.END, f"{word.upper()}\n")

# Layout
tk.Label(root, text="Next Best Guess:").grid(row=0, column=0, sticky="w")
best_guess = tk.StringVar()
tk.Entry(root, textvariable=best_guess, width=10).grid(row=0, column=1)
suggest_button = tk.Button(root, text="Suggest Guess", command=suggest_next_guess)
suggest_button.grid(row=0, column=2)
suggest_button.config(state="disabled")

tk.Button(root, text="Restart Solver", command=restart_solver).grid(row=0, column=3)

tk.Label(root, text="Enter Feedback:").grid(row=1, column=0, sticky="w")
feedback_frame = tk.Frame(root)
feedback_frame.grid(row=1, column=1, columnspan=3)

for i in range(5):
    btn = tk.Button(feedback_frame, text=fb_display['B'], width=3, bg=tile_colors['B'],
                    command=lambda i=i: cycle_feedback(i))
    btn.grid(row=0, column=i, padx=2)
    feedback_buttons.append(btn)

tk.Button(root, text="Apply Feedback", command=apply_feedback).grid(row=2, column=0, columnspan=4, pady=5)

tk.Label(root, text="Guess Log:").grid(row=3, column=0, sticky="w")
guess_log = tk.Text(root, width=50, height=10)
guess_log.grid(row=4, column=0, columnspan=4)

tk.Label(root, text="Top 5 Suggestions:").grid(row=5, column=0, sticky="w")
top5_output = tk.Text(root, width=50, height=8)
top5_output.grid(row=6, column=0, columnspan=4)

tk.Label(root, text="Remaining Candidates:").grid(row=7, column=0, sticky="w")
remaining_output = tk.Text(root, width=50, height=10)
remaining_output.grid(row=8, column=0, columnspan=4)

update_remaining_display()
root.mainloop()