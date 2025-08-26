# wordlist.py
import os
from wordfreq import word_frequency

def load_wordle_list(filename="wordle_list.txt"):
    path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(path, 'r') as f:
            return [line.strip().lower() for line in f if len(line.strip()) == 5]
    except Exception as e:
        raise RuntimeError(f"Failed to load word list: {e}")

def get_frequency(word):
    return word_frequency(word, 'en') or 0.00001