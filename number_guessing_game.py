#!/usr/bin/env python3
"""Number Guessing Game — play it from the terminal.

Usage:
    python3 number_guessing_game.py [--difficulty easy|medium|hard]

Pick a difficulty, then guess the secret number. After every guess you
get a "too low / too high" hint. Win before you run out of attempts
and you score points — fewer guesses, more points.
"""

import argparse
import sys

from guessing_game import DIFFICULTIES, FEEDBACK, Game, parse_guess, score


def choose_difficulty(argv: list[str]) -> str:
    parser = argparse.ArgumentParser(description="Number Guessing Game")
    parser.add_argument(
        "--difficulty", default="medium", choices=sorted(DIFFICULTIES),
        help="easy: 1-50 in 10 tries, medium: 1-100 in 7 tries, "
             "hard: 1-500 in 5 tries (default: medium)")
    return parser.parse_args(argv).difficulty


def play_round(difficulty: str) -> None:
    game = Game(difficulty)
    print(f"\nI'm thinking of a number between {game.low} and {game.high}.")
    print(f"You have {game.max_attempts} attempts. Good luck!\n")

    while not game.over:
        try:
            raw = input(f"Guess ({game.attempts_left} left): ")
        except (EOFError, KeyboardInterrupt):
            print("\nGame interrupted. The number was", game.secret)
            return
        try:
            guess = parse_guess(raw, game.low, game.high)
        except ValueError as exc:
            print(exc)
            continue
        result = game.guess(guess)
        print(FEEDBACK[result])
        if result == "correct":
            print(f"You won in {game.attempts} "
                  f"{'try' if game.attempts == 1 else 'tries'}! "
                  f"Score: {score(game.attempts, game.max_attempts)}")
            return
    print(f"\nOut of attempts! The number was {game.secret}.")


def main(argv: list[str] | None = None) -> int:
    difficulty = choose_difficulty(sys.argv[1:] if argv is None else argv)
    while True:
        play_round(difficulty)
        try:
            again = input("\nPlay again? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if again not in ("y", "yes"):
            break
    print("Thanks for playing!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
