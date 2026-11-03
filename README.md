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
The interface offers **Play round** and **New game**. Higher-ranked
cards win each round; equal ranks trigger a war with three face-down
cards before the next comparison. The winner collects the contested cards.

## Testing

```sh
python3 -m unittest discover -s tests -v
```

Five offline tests check all 52 card images, unique decks, conservation
of cards over thousands of rounds, tied-card wars and invalid cards.
The Tkinter GUI was also launched, played one round and reset on Manjaro.

The original 2019 EasyGUI implementation remains in branch `old`.
