# main.py
import tkinter as tk
from collections import defaultdict
from wordlist import load_wordle_list
from feedback import get_feedback, update_constraints
from solver import rank_suggestions, filter_candidates, get_frequency, prefilter_grays

wordle_list = load_wordle_list()
candidates = wordle_list.copy()
greens = {}
yellows = defaultdict(set)
grays = set()
mode = "entropy"
fb_state = ['B'] * 5
fb_display = {'G': '🟩', 'Y': '🟨', 'B': '⬜'}
tile_colors = {'G': '#6aaa64', 'Y': '#c9b458', 'B': '#787c7e'}


root = tk.Tk()
root.title("Wordle Solver (Hard Mode)")
root.geometry("600x700")  # Wider default
root.columnconfigure(0, weight=1)

letter_vars = [tk.StringVar() for _ in range(5)]
letter_boxes = []
feedback_buttons = []
full_word_var = tk.StringVar()

def fill_letter_boxes(*args):
    word = full_word_var.get().lower()
    for i in range(5):
        letter_vars[i].set(word[i] if i < len(word) else "")

def cycle_feedback(i):
    order = {'B': 'Y', 'Y': 'G', 'G': 'B'}
    fb_state[i] = order[fb_state[i]]
    feedback_buttons[i].config(text=fb_display[fb_state[i]], bg=tile_colors[fb_state[i]])

def keypress(event):
    if event.char in '12345':
        i = int(event.char) - 1
        cycle_feedback(i)

def animate_suggestion(word):
    for i in range(5):
        letter_vars[i].set(word[i].upper())
        letter_boxes[i].config(bg="#d3d3d3")
    root.after(150, reset_tile_colors)

def reset_tile_colors():
    for box in letter_boxes:
        box.config(bg="white")

def apply():
    global mode
    guess = ''.join([var.get().lower() for var in letter_vars])
    if len(guess) != 5:
        return
    feedback = ''.join(fb_state)
    update_constraints(guess, feedback, greens, yellows, grays)
    global candidates
    candidates = filter_candidates(candidates, guess, feedback, greens, yellows, grays)
    guess_log.insert(tk.END, f"{guess.upper()} → {''.join([fb_display[f] for f in fb_state])}\n")
    full_word_var.set("")
    for i in range(5):
        fb_state[i] = 'B'
        feedback_buttons[i].config(text=fb_display['B'], bg=tile_colors['B'])
    update_remaining()

    # Switch to fast mode if first guess is all gray
    if feedback == "BBBBB" and not greens and not yellows:
        mode = "fast"
    else:
        mode = "entropy"

    auto_suggest()

def auto_suggest():
    if not candidates:
        guess_log.insert(tk.END, "No candidates remaining. Solver cannot proceed.\n")
        top5_output.delete(1.0, tk.END)
        top5_output.insert(tk.END, "No suggestions available.\n")
        return

    if mode == "fast":
        filtered = prefilter_grays(candidates, {}, defaultdict(set), grays)
        top5 = sorted(
            [(w, get_frequency(w)) for w in filtered],
            key=lambda x: x[1],
            reverse=True
        )[:5]
        top5 = [(w, 0, 0, freq) for w, freq in top5]  # Pad with dummy entropy
        guess_log.insert(tk.END, f"Fast mode: avoiding grays {', '.join(sorted(grays))}\n")
    else:
        top5 = rank_suggestions(candidates, greens, yellows, grays)

    if not top5:
        guess_log.insert(tk.END, "No valid suggestions.\n")
        top5_output.delete(1.0, tk.END)
        top5_output.insert(tk.END, "No suggestions available.\n")
        return

    animate_suggestion(top5[0][0])
    guess_log.insert(tk.END, f"Suggested: {top5[0][0].upper()} (Entropy: {top5[0][2]:.3f}, Freq: {top5[0][3]:.6f})\n")
    top5_output.delete(1.0, tk.END)
    for word, score, ent, freq in top5:
        top5_output.insert(tk.END, f"{word.upper():<8} Score: {score:.6f} | Entropy: {ent:.3f} | Freq: {freq:.6f}\n")

def restart():
    global candidates, greens, yellows, grays, mode
    candidates = wordle_list.copy()
    greens.clear()
    yellows.clear()
    grays.clear()
    mode = "entropy"
    full_word_var.set("")
    guess_log.delete(1.0, tk.END)
    top5_output.delete(1.0, tk.END)
    remaining_output.delete(1.0, tk.END)
    for i in range(5):
        letter_vars[i].set("")
        fb_state[i] = 'B'
        feedback_buttons[i].config(text=fb_display['B'], bg=tile_colors['B'])
    update_remaining()

def update_remaining():
    remaining_output.delete(1.0, tk.END)
    remaining_output.insert(tk.END, f"Remaining: {len(candidates)}\n")
    for word in candidates[:20]:
        remaining_output.insert(tk.END, f"{word.upper()}\n")

# Layout

# Create a frame to hold label and entry side by side

# Validation function to allow only letters
def validate_letters(P):
    return P.isalpha() or P == ""

vcmd = (root.register(validate_letters), '%P')

word_entry_frame = tk.Frame(root)
word_entry_frame.grid(row=0, column=0, sticky="w")
tk.Label(word_entry_frame, text="Enter Word:").pack(side="left")
full_word_entry = tk.Entry(word_entry_frame, textvariable=full_word_var, width=10, validate="key", validatecommand=vcmd)
full_word_entry.pack(side="left")
full_word_var.trace_add("write", fill_letter_boxes)

tk.Button(root, text="Restart", command=restart).grid(row=0, column=1)

letter_frame = tk.Frame(root)
letter_frame.grid(row=1, column=0, columnspan=5, pady=10)

for i in range(5):
    entry = tk.Entry(letter_frame, textvariable=letter_vars[i], width=2, justify='center',
                     font=('Helvetica', 18), state="readonly")
    entry.grid(row=0, column=i, padx=5)
    letter_boxes.append(entry)

feedback_frame = tk.Frame(root)
feedback_frame.grid(row=2, column=0, columnspan=5)

for i in range(5):
    btn = tk.Button(feedback_frame, text=fb_display['B'], width=3, bg=tile_colors['B'],
                    command=lambda i=i: cycle_feedback(i))
    btn.grid(row=0, column=i, padx=5)
    feedback_buttons.append(btn)

apply_button = tk.Button(root, text="Apply Feedback", command=apply)
apply_button.grid(row=3, column=0, columnspan=5, pady=5)
def check_apply_button(*args):
    filled = all(len(var.get()) == 1 and var.get().isalpha() for var in letter_vars)
    if filled:
        apply_button.config(state="normal")
    else:
        apply_button.config(state="disabled")

for var in letter_vars:
    var.trace_add("write", check_apply_button)
apply_button.config(state="disabled")

tk.Label(root, text="Guess Log:").grid(row=4, column=0, sticky="w")
guess_log = tk.Text(root, width=50, height=10)
guess_log.grid(row=5, column=0, columnspan=5)

tk.Label(root, text="Top 5 Suggestions:").grid(row=6, column=0, sticky="w")
top5_output = tk.Text(root, width=70, height=8)
top5_output.grid(row=7, column=0, columnspan=5)

tk.Label(root, text="Remaining Candidates:").grid(row=8, column=0, sticky="w")
remaining_output = tk.Text(root, width=70, height=10)
remaining_output.grid(row=9, column=0, columnspan=5)

def launch():
    update_remaining()
    root.bind("<Key>", keypress)
    root.mainloop()

if __name__ == "__main__":
    launch()