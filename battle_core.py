#!/usr/bin/env python3
# Developer: Hamdy Abou El Anein
# Contact: hamdy.aea@protonmail.com
# SPDX-License-Identifier: GPL-3.0-or-later
"""Pure Python model for the card game War (Battle), with deterministic tests."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import random


RANKS = tuple(range(2, 15))
SUITS = ("Carreaux", "Coeur", "Piques", "treffles")


@dataclass(frozen=True, order=True)
class Card:
    rank: int
    suit: str

    def __post_init__(self):
        if self.rank not in RANKS or self.suit not in SUITS:
            raise ValueError("Invalid playing card")

    @property
    def name(self) -> str:
        faces = {11: "Valet", 12: "Reine", 13: "Roi", 14: "As"}
        return f"{faces.get(self.rank, self.rank)} {self.suit}"


@dataclass(frozen=True)
class Round:
    player_card: Card | None
    computer_card: Card | None
    winner: str | None
    war: bool
    cards_at_stake: int
    game_over: bool


class BattleGame:
    """Standard 52-card War: higher card wins; tied cards trigger a war."""

    def __init__(self, *, seed: int | None = None):
        self.rng = random.Random(seed)
        deck = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        self.rng.shuffle(deck)
        self.player = deque(deck[:26])
        self.computer = deque(deck[26:])
        self.rounds = 0

    @property
    def winner(self) -> str | None:
        if not self.player and not self.computer:
            return "draw"
        if not self.player:
            return "computer"
        if not self.computer:
            return "player"
        return None

    def play_round(self) -> Round:
        if self.winner is not None:
            raise RuntimeError("Game is already over")
        self.rounds += 1
        pile: list[Card] = []
        player_face: Card | None = None
        computer_face: Card | None = None
        war = False
        while True:
            if not self.player or not self.computer:
                winner = self.winner or ("player" if self.player else "computer")
                break
            player_face = self.player.popleft()
            computer_face = self.computer.popleft()
            pile.extend((player_face, computer_face))
            if player_face.rank > computer_face.rank:
                winner = "player"
                break
            if player_face.rank < computer_face.rank:
                winner = "computer"
                break
            war = True
            # Each player stakes one hidden card before the next comparison.
            if self.player and self.computer:
                pile.extend((self.player.popleft(), self.computer.popleft()))
            if not self.player or not self.computer:
                winner = "player" if self.player else "computer" if self.computer else "draw"
                break
        if winner == "player":
            self.rng.shuffle(pile)
            self.player.extend(pile)
        elif winner == "computer":
            self.rng.shuffle(pile)
            self.computer.extend(pile)
        # In a draw with both hands exhausted, the pile is split evenly.
        else:
            self.rng.shuffle(pile)
            half = len(pile) // 2
            self.player.extend(pile[:half])
            self.computer.extend(pile[half:])
        assert len(self.player) + len(self.computer) == 52, "Lost or duplicated cards"
        return Round(player_face, computer_face, winner, war, len(pile),
                     self.winner is not None)
