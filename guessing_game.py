"""Number Guessing Game — core game logic.

The game picks a secret number and the player tries to guess it.
All logic here is pure (no input()/print()), so it can be tested
without a terminal. The CLI lives in ``number_guessing_game.py``.
"""

import random

DIFFICULTIES = {
    "easy": {"low": 1, "high": 50, "max_attempts": 10},
    "medium": {"low": 1, "high": 100, "max_attempts": 7},
    "hard": {"low": 1, "high": 500, "max_attempts": 5},
}

FEEDBACK = {
    "too_low": "Too low! Try a bigger number.",
    "too_high": "Too high! Try a smaller number.",
    "correct": "Correct!",
}


def pick_secret(low: int, high: int, rng: random.Random | None = None) -> int:
    """Return a random secret number in the inclusive range [low, high]."""
    rng = rng or random
    return rng.randint(low, high)


def evaluate_guess(secret: int, guess: int) -> str:
    """Classify a guess: 'too_low', 'too_high', or 'correct'."""
    if guess < secret:
        return "too_low"
    if guess > secret:
        return "too_high"
    return "correct"


def parse_guess(raw: str, low: int, high: int) -> int:
    """Parse and validate a guess string.

    Raises ValueError with a friendly message for non-numbers or
    out-of-range values.
    """
    try:
        guess = int(raw.strip())
    except ValueError:
        raise ValueError("Please enter a whole number.") from None
    if not low <= guess <= high:
        raise ValueError(f"Please enter a number between {low} and {high}.")
    return guess


def score(attempts_used: int, max_attempts: int) -> int:
    """Score a win: 100 points minus 10 per extra attempt, minimum 10."""
    return max(10, 100 - 10 * (attempts_used - 1))


class Game:
    """One round of the guessing game."""

    def __init__(self, difficulty: str = "medium", secret: int | None = None,
                 rng: random.Random | None = None):
        if difficulty not in DIFFICULTIES:
            raise ValueError(f"Unknown difficulty: {difficulty!r}. "
                             f"Choose one of {sorted(DIFFICULTIES)}.")
        cfg = DIFFICULTIES[difficulty]
        self.low, self.high = cfg["low"], cfg["high"]
        self.max_attempts = cfg["max_attempts"]
        self.secret = secret if secret is not None else pick_secret(
            self.low, self.high, rng)
        self.attempts = 0
        self.won = False

    @property
    def attempts_left(self) -> int:
        return self.max_attempts - self.attempts

    def guess(self, value: int) -> str:
        """Make a guess; returns 'too_low', 'too_high', or 'correct'."""
        self.attempts += 1
        result = evaluate_guess(self.secret, value)
        if result == "correct":
            self.won = True
        return result

    @property
    def over(self) -> bool:
        return self.won or self.attempts >= self.max_attempts
