# Arcade Games

Some simple games written with
[Python Arcade](https://arcade.academy/).


# The Games

## `find_fastest_way.py`

Hlep the frog to get to his little green friend.
Control the frog using the up/down/left/right keys on your keyboard.
Do not hit the obstacles.
But you can make them disappear -- press Space.
Try to make it to the goal with as few distance traveled as possible and as few obstacles removed.

Use `N` to start a new game, `R` to restart the current one and `Q` to quit.

## `schatzsuche.py`

Find the gold.
Click on a tile to reveal a tip or to find the gold.
A tip is an arrow pointing in the general direction of the gold.
If it points left, the gold is left of that tile -- but it could be left and above or left and below etc.

Use `Q` to quit.

## `schiffe_versenken.py`

Play battleship against a computer.
Check the command line output for what you need to search.

Use `Q` to quit.

## `grid_based_game.py`

Not actually a game but rather a demo/template for a grid based game.
`schatzsuche.py` is based upon that.



# License

The code in this repository is MIT licensed, see
[LICENSE](LICENSE).

The games base on other games that are also MIT licensed by

    Copyright (c) 2020 Paul Vincent Craven


# Known Issues

On Linux you might get a crash when drawing a text with a core dump from
`munmap_chunk`.
To fix this, run
(see [here](https://github.com/python-pillow/Pillow/issues/4225#issuecomment-605769767)):

    pip uninstall PilloW
    pip install --compile --install-option=-O1 PilloW
