"""Tests for the Number Guessing Game (guessing_game.py)."""

import unittest
from unittest.mock import patch
import random

from guessing_game import (
    DIFFICULTIES, Game, evaluate_guess, parse_guess, pick_secret, score,
)


class TestEvaluateGuess(unittest.TestCase):
    def test_too_low(self):
        self.assertEqual(evaluate_guess(50, 10), "too_low")

    def test_too_high(self):
        self.assertEqual(evaluate_guess(50, 90), "too_high")

    def test_correct(self):
        self.assertEqual(evaluate_guess(50, 50), "correct")


class TestParseGuess(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(parse_guess("42", 1, 100), 42)

    def test_whitespace_ok(self):
        self.assertEqual(parse_guess("  7  ", 1, 100), 7)

    def test_non_number_rejected(self):
        with self.assertRaises(ValueError):
            parse_guess("abc", 1, 100)

    def test_float_rejected(self):
        with self.assertRaises(ValueError):
            parse_guess("4.5", 1, 100)

    def test_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            parse_guess("0", 1, 100)
        with self.assertRaises(ValueError):
            parse_guess("101", 1, 100)


class TestPickSecret(unittest.TestCase):
    def test_within_range(self):
        for _ in range(200):
            self.assertTrue(1 <= pick_secret(1, 100) <= 100)

    def test_seeded_rng_reproducible(self):
        a = pick_secret(1, 100, random.Random(7))
        b = pick_secret(1, 100, random.Random(7))
        self.assertEqual(a, b)


class TestGame(unittest.TestCase):
    def test_win_flow(self):
        game = Game("medium", secret=42)
        self.assertEqual(game.guess(10), "too_low")
        self.assertEqual(game.guess(90), "too_high")
        self.assertFalse(game.over)
        self.assertEqual(game.guess(42), "correct")
        self.assertTrue(game.won)
        self.assertTrue(game.over)

    def test_loss_after_max_attempts(self):
        game = Game("easy", secret=42)  # 10 attempts
        for _ in range(10):
            game.guess(1)
        self.assertFalse(game.won)
        self.assertTrue(game.over)

    def test_attempts_left_counts_down(self):
        game = Game("hard", secret=42)  # 5 attempts
        game.guess(1)
        self.assertEqual(game.attempts_left, 4)

    def test_unknown_difficulty_rejected(self):
        with self.assertRaises(ValueError):
            Game("impossible")

    def test_difficulty_ranges(self):
        self.assertEqual((Game("easy").low, Game("easy").high), (1, 50))
        self.assertEqual((Game("medium").low, Game("medium").high), (1, 100))
        self.assertEqual((Game("hard").low, Game("hard").high), (1, 500))


class TestScore(unittest.TestCase):
    def test_first_try_is_100(self):
        self.assertEqual(score(1, 7), 100)

    def test_later_attempts_drop(self):
        self.assertEqual(score(3, 7), 80)

    def test_minimum_is_10(self):
        self.assertEqual(score(99, 10), 10)


class TestCLI(unittest.TestCase):
    def test_play_round_win(self):
        with patch("number_guessing_game.Game") as MockGame, \
                patch("builtins.input", side_effect=["10", "42", "n"]), \
                patch("builtins.print"):
            game = MockGame.return_value
            game.low, game.high, game.max_attempts = 1, 100, 7
            game.attempts_left = 7
            game.over = False
            game.guess.side_effect = ["too_low", "correct"]
            game.attempts = 2
            import number_guessing_game
            number_guessing_game.play_round("medium")
            self.assertEqual(game.guess.call_count, 2)


if __name__ == "__main__":
    unittest.main()
