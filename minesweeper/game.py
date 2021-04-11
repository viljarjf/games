import numpy as np
import tkinter
from enum import IntEnum
from typing import Tuple

from numpy.lib.shape_base import tile

class TileState(IntEnum):

    flagged = -3
    bomb = -2
    unchecked = -1

    none = 0
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8


class MineSweeper:

    def __init__(self, height: int, width: int, mines: int):
        self._shape = self._height, self._width = height, width
        self._mine_amount = mines

        # let's make a whacky initialization method shall we?
        self._minemap = np.zeros(self._shape).astype(bool).flatten()
        self._minemap[:mines] = True
        np.random.shuffle(self._minemap)
        self._minemap = self._minemap.reshape(self._shape)

        self._current_game_state = np.zeros(self._shape) + TileState.unchecked
    

    def get_tile_state(self, pos: Tuple[int, int]) -> TileState:
        return TileState(self._current_game_state[pos])
    

    def _flip_single_tile(self, pos: Tuple[int, int]) -> bool:
        if self._minemap[pos]:
            self._current_game_state[pos] = TileState.bomb
            return True

        y, x = pos
        y_max, x_max = self._shape
        n_bombs = np.count_nonzero(self._minemap[
            max(0, y-1) : min(y_max, y+2),
            max(0, x-1) : min(x_max, x+2)
            ])
        self._current_game_state[pos] = n_bombs
        return False


    def flip_tile(self, pos: Tuple[int, int]) -> bool:
        if state := self._current_game_state[pos] != TileState.unchecked:
            return state == TileState.bomb

        if is_bomb := self._flip_single_tile(pos):
            return True
        
        y, x = pos
        y_max, x_max = self._shape
        n_flagged = np.count_nonzero(
            self._minemap[
                max(0, y-1) : min(y_max, y+2),
                max(0, x-1) : min(x_max, x+2)
            ]
            == TileState.flagged
        )
        states = [is_bomb]
        if n_flagged == self._current_game_state[pos]:
            for _y in range(max(0, y-1) , min(y_max, y+2)):
                for _x in range(max(0, x-1), min(x_max, x+2)):
                    states.append(self.flip_tile((_y, _x)))
        return max(states)


    def test(self):
        print(self._minemap)
        print()
        print(self._current_game_state)
        s = self.flip_tile((3,3))
        print(self._current_game_state)
        print(s)


game = MineSweeper(10, 10, 10)
game.test()