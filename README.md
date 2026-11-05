# Battle Cards — Python War Game

Developer: Hamdy Abou El Anein
Contact: hamdy.aea@protonmail.com
License: GNU GPL v3 (see LICENSE).

A classic 52-card **War** game against the computer, rewritten with
Tkinter instead of EasyGUI. The original artwork is retained and shown
using Pillow. Original images may have separate third-party rights;
this rewrite does not claim authorship of those images.

## Run

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python battle.py
```

Tkinter must be installed by your Linux distribution (usually `tk`).
The interface offers **Play round** and **New game**. Ranks from highest to lowest are
Ace, King, Queen, Jack, 10, 9, 8, 7, 6, 5, 4, 3, 2. On a tie, each player
places one card face down and turns over the next. Another tie repeats this
sequence on the same pile. Click **Continue battle** to place the hidden cards,
then click again to reveal the next pair. After each round, scroll through
the captured cards to see their pictures and English names. The higher revealed card wins the entire pile.

## Testing

```sh
python3 -m unittest discover -s tests -v
```

Offline tests check all 52 card images, unique decks, conservation
of cards over thousands of rounds, tied-card wars and invalid cards.
The Tkinter GUI was also launched, played one round and reset on Manjaro.

The original 2019 EasyGUI implementation remains in branch `old`.
