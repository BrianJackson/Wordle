# main.py
import tkinter as tk
from collections import defaultdict
from wordlist import load_wordle_list
from feedback import get_feedback, update_constraints
from solver import rank_suggestions, filter_candidates

wordle_list = load_wordle_list()
candidates = wordle_list.copy()
greens = {}
yellows = defaultdict(set)
grays = set()
fb_state = ['B'] * 5
fb_display = {'G': '🟩', 'Y': '🟨', 'B': '⬜'}
tile_colors = {'G': '#6aaa64', 'Y': '#c9b458', 'B': '#787c7e'}

root = tk.Tk()
root.title("Wordle Solver")

def suggest():
    top5 = rank_suggestions(candidates, greens, yellows, grays)
    if not top5:
        guess_log.insert(tk.END, "No valid suggestions.\n")
        return
    best_guess.set(top5[0][0].upper())
    guess_log.insert(tk.END, f"Suggested: {top5[0][0].upper()} (Entropy: {top5[0][2]:.3f}, Freq: {top5[0][3]:.6f})\n")
    top5_output.delete(1.0, tk.END)
    for word, score, ent, freq in top5:
        top5_output.insert(tk.END, f"{word.upper():<8} Score: {score:.6f} | Entropy: {ent:.3f} | Freq: {freq:.6f}\n")

def apply():
    guess = best_guess.get().lower()
    if len(guess) != 5:
        return
    feedback = ''.join(fb_state)
    update_constraints(guess, feedback, greens, yellows, grays)
    global candidates
    candidates = filter_candidates(candidates, guess, feedback, greens, yellows, grays)
    guess_log.insert(tk.END, f"{guess.upper()} → {''.join([fb_display[f] for f in fb_state])}\n")
    best_guess.set("")
    for i in range(5):
        fb_state[i] = 'B'
        fb_buttons[i].config(text=fb_display['B'], bg=tile_colors['B'])
    update_remaining()

def restart():
    global candidates, greens, yellows, grays
    candidates = wordle_list.copy()
    greens.clear()
    yellows.clear()
    grays.clear()
    best_guess.set("")
    guess_log.delete(1.0, tk.END)
    top5_output.delete(1.0, tk.END)
    remaining_output.delete(1.0, tk.END)
    for i in range(5):
        fb_state[i] = 'B'
        fb_buttons[i].config(text=fb_display['B'], bg=tile_colors['B'])
    update_remaining()

def cycle(i):
    order = {'B': 'Y', 'Y': 'G', 'G': 'B'}
    fb_state[i] = order[fb_state[i]]
    fb_buttons[i].config(text=fb_display[fb_state[i]], bg=tile_colors[fb_state[i]])

def update_remaining():
    remaining_output.delete(1.0, tk.END)
    remaining_output.insert(tk.END, f"Remaining: {len(candidates)}\n")
    for word in candidates[:20]:
        remaining_output.insert(tk.END, f"{word.upper()}\n")

tk.Label(root, text="Next Guess:").grid(row=0, column=0)
best_guess = tk.StringVar()
tk.Entry(root, textvariable=best_guess, width=10).grid(row=0, column=1)
tk.Button(root, text="Suggest", command=suggest).grid(row=0, column=2)
tk.Button(root, text="Restart", command=restart).grid(row=0, column=3)

tk.Label(root, text="Feedback:").grid(row=1, column=0)
fb_frame = tk.Frame(root)
fb_frame.grid(row=1, column=1, columnspan=3)
fb_buttons = []
for i in range(5):
    btn = tk.Button(fb_frame, text=fb_display['B'], width=3, bg=tile_colors['B'], command=lambda i=i: cycle(i))
    btn.grid(row=0, column=i)
    fb_buttons.append(btn)

tk.Button(root, text="Apply Feedback", command=apply).grid(row=2, column=0, columnspan=4)

tk.Label(root, text="Guess Log:").grid(row=3, column=0)
guess_log = tk.Text(root, width=50, height=10)
guess_log.grid(row=4, column=0, columnspan=4)

tk.Label(root, text="Top 5 Suggestions:").grid(row=5, column=0)
top5_output = tk.Text(root, width=50, height=8)
top5_output.grid(row=6, column=0, columnspan=4)

tk.Label(root, text="Remaining Candidates:").grid(row=7, column=0)
remaining_output = tk.Text(root, width=50, height=10)
remaining_output.grid(row=8, column=0, columnspan=4)

def launch():
    update_remaining()
    root.mainloop()

if __name__ == "__main__":
    launch()