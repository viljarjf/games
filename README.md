# games

## chess 

multidimensional chess, made as abstractly as possible to make it easier to specialise into different dimensions.

Everything necessary to make a new-dimension-implementation should be clear from the two examples in `chess/games`, but will be summarized here as well: Override the three abstract methods in the `NDChessGUI`-class, and initiate the board.

Graphics implemented with tkinter. Future plans for a web port with Flask. 

Install the packages in `requirements.txt` before playing, e.g. `python3 -m pip install -r chess/requirements.txt`

## 2048

complete. Small bug with double summing when 0422 -> 0008 for example

## pest as 

disease game, heavily inspired by plague inc, but the map is of gløshaugen. Unfinished
