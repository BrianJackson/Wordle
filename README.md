# 🧠  Wordle Solver

A Python-based Wordle solver that uses entropy and word frequency to suggest optimal guesses. Includes both a GUI and CLI interface, with full hard mode enforcement.

---

## 📦 Features

- ✅ Modular architecture (GUI, CLI, logic, feedback, wordlist)
- ✅ Positional enforcement (green/yellow/gray constraints)
- ✅ Entropy × frequency scoring for smart suggestions
- ✅ Top 5 guess recommendations
- ✅ CLI support for terminal-based solving
- ✅ Unit tests for feedback and solver logic

---

## 🖥️ GUI Usage

🧠 Click the boxes to provide feedback on the current guess in the text box
The solver enforces logical consistency across guesses:
- 🟩 Green letters must stay in the same position
- 🟨 Yellow letters must be reused, but not in the same position
- ⬜ Gray letters must be excluded from future guesses (unless confirmed as green/yellow)
This ensures every guess builds on known information and avoids wasteful plays.

Run the GUI with:

```bash
python main.py

## 🧪 CLI Usage
Run the solver from the terminal:
python cli.py --guess crane --feedback BYGBY


🎯 CLI Feedback Format
Each letter in the feedback string corresponds to the result of your guess:
- B = Gray (letter not in the word)
- Y = Yellow (letter is in the word but wrong position)
- G = Green (letter is correct and in the correct position)


Example:
python cli.py --guess crane --feedback BYGBY
Means:
- C = not in the word
- R = in the word, wrong position
- A = correct position
- N = not in the word
- E = in the word, wrong position
The CLI will return:
- Number of remaining candidates
- Top 5 suggestions with entropy × frequency scores

🧪 Running Tests
Unit tests are located in the tests/ folder. Run all tests with:
python -m unittest discover tests



📁 Folder Structure
wordle/
├── main.py          # GUI entry point
├── cli.py           # Command-line interface
├── wordlist.py      # Word list and frequency scoring
├── feedback.py      # Feedback logic and hard mode
├── solver.py        # Entropy and filtering
├── wordle_list.txt  # Word list (5-letter words) from https://github.com/tabatkins/wordle-list/blob/main/words
├── __init__.py      # Package initializer
└── tests/
    ├── test_feedback.py
    └── test_solver.py



📌 Requirements
- Python 3.8+
- wordfreq library:
pip install wordfreq



🧠 Hard Mode Explained
Hard mode enforces logical consistency across guesses:
- 🟩 Green letters must stay in the same position
- 🟨 Yellow letters must be reused, but not in the same position
- ⬜ Gray letters must be excluded from future guesses (unless confirmed as green/yellow)
This ensures every guess builds on known information and avoids wasteful plays.

🚀 Future Ideas
- Toggle for hard mode on/off
- Export guess history
- Visual entropy distribution
- Solver API for integration

Happy solving!

---

Let me know if you want this README embedded in the GUI or printed from the CLI with a `--help` flag. We can keep refining this into a full-featured Wordle toolkit.


