# cli.py
import argparse
from collections import defaultdict
from wordlist import load_wordle_list
from feedback import update_constraints
from solver import rank_suggestions, filter_candidates
from version import __version__

def main():
    parser = argparse.ArgumentParser(description=f"Wordle Solver CLI v{__version__}")
    parser.add_argument("--guess", type=str, help="Your guess word (5 letters)")
    parser.add_argument("--feedback", type=str, help="Feedback string (e.g. BYGBY)")
    parser.add_argument("--version", action="version", version=f"Wordle Solver v{__version__}")
    args = parser.parse_args()

    if not args.guess or not args.feedback or len(args.guess) != 5 or len(args.feedback) != 5:
        print("Usage: python cli.py --guess crane --feedback BYGBY")
        return

    wordle_list = load_wordle_list()
    candidates = wordle_list.copy()
    greens = {}
    yellows = defaultdict(set)
    grays = set()

    update_constraints(args.guess.lower(), args.feedback.upper(), greens, yellows, grays)
    candidates = filter_candidates(candidates, args.guess.lower(), args.feedback.upper(), greens, yellows, grays)

    print(f"\nRemaining candidates: {len(candidates)}")
    print("Top suggestions:")
    for word, score, entropy, freq in rank_suggestions(candidates, greens, yellows, grays):
        print(f"{word.upper():<8} Score: {score:.6f} | Entropy: {entropy:.3f} | Freq: {freq:.6f}")

if __name__ == "__main__":
    main()