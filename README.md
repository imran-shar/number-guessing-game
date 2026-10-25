# Number Guessing Game (Python)

A classic beginner Python project: the computer picks a secret number and
you try to guess it, with "too low / too high" hints after every guess.

## How to play

```bash
python3 number_guessing_game.py
```

Or pick a difficulty:

```bash
python3 number_guessing_game.py --difficulty easy    # 1–50, 10 attempts
python3 number_guessing_game.py --difficulty medium  # 1–100, 7 attempts (default)
python3 number_guessing_game.py --difficulty hard    # 1–500, 5 attempts
```

Win before you run out of attempts and you score points — the fewer
guesses you use, the higher your score (100 for a first-try win, down
to a minimum of 10). Type `n` when asked to play again to quit.

## Run the tests

```bash
python3 -m unittest test_number_guessing_game.py -v
```

No third-party packages needed — Python 3.10+ standard library only.

## What you learn

- `while` loops and loop exit conditions
- `if / elif / else` conditionals
- `random.randint` for the secret number
- Input validation (non-numbers and out-of-range guesses are rejected
  without crashing, and bad input does not cost an attempt)
- Separating pure game logic (`guessing_game.py`) from the terminal UI
  (`number_guessing_game.py`) so the logic can be unit-tested
- `argparse` for command-line options
- Unit testing with `unittest` and `unittest.mock`

## Project structure

```
number_guessing_game.py       # terminal UI: prompts, hints, replay loop
guessing_game.py              # pure game logic: Game class, scoring, validation
test_number_guessing_game.py  # unit tests for the logic and the CLI
```

## Ideas to extend it

- Add a "very close!" hint when a guess is within 5 of the secret
- Keep a high-score table in a JSON file
- Add a two-player mode where one player sets the secret number
