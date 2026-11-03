#!/usr/bin/env python3
# Developer: Hamdy Abou El Anein
# Contact: hamdy.aea@protonmail.com
# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline model and card-artwork regression tests."""
from collections import deque
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from battle_core import BattleGame, Card, RANKS, SUITS
from battle import image_filename


class BattleTests(unittest.TestCase):
    def test_52_unique_cards(self):
        game = BattleGame(seed=1)
        deck = list(game.player) + list(game.computer)
        self.assertEqual(len(deck), 52)
        self.assertEqual(len(set(deck)), 52)

    def test_cards_never_lost(self):
        for seed in range(15):
            game = BattleGame(seed=seed)
            for _ in range(1500):
                if game.winner is not None:
                    break
                result = game.play_round()
                cards = list(game.player) + list(game.computer)
                self.assertEqual(len(cards), 52)
                self.assertEqual(len(set(cards)), 52)
                self.assertEqual(result.game_over, game.winner is not None)

    def test_war_takes_all_staked_cards(self):
        game = BattleGame(seed=3)
        game.player = deque([Card(8, "Coeur"), Card(2, "Coeur"),
                             Card(3, "Coeur"), Card(4, "Coeur"),
                             Card(13, "Coeur")])
        game.computer = deque([Card(8, "Piques"), Card(2, "Piques"),
                               Card(3, "Piques"), Card(4, "Piques"),
                               Card(12, "Piques")])
        # Complete the two decks with the other 42 distinct cards.
        used = set(game.player) | set(game.computer)
        rest = [Card(rank, suit) for rank in RANKS for suit in SUITS
                if Card(rank, suit) not in used]
        game.player.extend(rest[:21])
        game.computer.extend(rest[21:])
        outcome = game.play_round()
        self.assertTrue(outcome.war)
        self.assertEqual(outcome.winner, "player")
        self.assertEqual(outcome.cards_at_stake, 10)
        self.assertEqual(len(game.player), 31)
        self.assertEqual(len(game.computer), 21)

    def test_all_artwork_paths_exist(self):
        root = Path(__file__).resolve().parents[1] / "Pictures"
        missing = [
            image_filename(Card(rank, suit))
            for rank in RANKS for suit in SUITS
            if not (root / image_filename(Card(rank, suit))).is_file()
        ]
        self.assertEqual(missing, [])

    def test_invalid_card(self):
        with self.assertRaises(ValueError):
            Card(15, "Coeur")


if __name__ == "__main__":
    unittest.main()
