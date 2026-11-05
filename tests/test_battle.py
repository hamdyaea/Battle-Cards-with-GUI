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

    def deal(self, player_ranks, computer_ranks):
        game = BattleGame(seed=3)
        game.player = deque(Card(rank, "Coeur") for rank in player_ranks)
        game.computer = deque(Card(rank, "Piques") for rank in computer_ranks)
        used = set(game.player) | set(game.computer)
        rest = [Card(rank, suit) for rank in RANKS for suit in SUITS
                if Card(rank, suit) not in used]
        split = 26 - len(game.player)
        game.player.extend(rest[:split])
        game.computer.extend(rest[split:])
        return game

    def test_war_takes_all_staked_cards(self):
        for player, computer in [
            ([8, 2, 13], [8, 14, 12]),
            ([8, 2, 9, 3, 13], [8, 14, 9, 10, 12]),
        ]:
            with self.subTest(player=player):
                game = self.deal(player, computer)
                stake = set(list(game.player)[:len(player)] +
                            list(game.computer)[:len(computer)])
                outcome = game.play_round()
                self.assertTrue(outcome.war)
                self.assertEqual(outcome.winner, "player")
                self.assertEqual(outcome.cards_at_stake, len(stake))
                self.assertEqual(set(list(game.player)[-len(stake):]), stake)

    def test_rank_order(self):
        ranks = [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        for high, low in zip(ranks, ranks[1:]):
            with self.subTest(high=high, low=low):
                self.assertEqual(self.deal([high], [low]).play_round().winner, "player")
                self.assertEqual(self.deal([low], [high]).play_round().winner, "computer")

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
