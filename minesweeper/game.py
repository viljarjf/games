import numpy as np
from enum import IntEnum
from typing import Tuple


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

        self._minemap = None

        self._current_game_state = np.zeros(self._shape, dtype = np.int32) + TileState.unchecked
    

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
        if (state := self._current_game_state[pos]) != TileState.unchecked:
            if state == TileState.bomb:
                return True
            elif state == TileState.none:
                return False
            elif state == TileState.flagged:
                return False

        # if this is the first click, ensure that it is not a bomb
        if self._minemap is None:
            # let's make a whacky initialization method shall we?
            self._minemap = np.zeros(self._shape).astype(bool).flatten()
            self._minemap[:self._mine_amount] = True
            np.random.shuffle(self._minemap)
            _pos = self._height*pos[0] + pos[1]
            while self._minemap[_pos]:
                np.random.shuffle(self._minemap)
            self._minemap = self._minemap.reshape(self._shape)
                
        is_flipped = (self._current_game_state[pos] >= 0)

        if (is_bomb := self._flip_single_tile(pos)) and not is_flipped:
            return True
        
        y, x = pos
        y_max, x_max = self._shape
        n_flagged = np.count_nonzero(
            self._current_game_state[
                max(0, y-1) : min(y_max, y+2),
                max(0, x-1) : min(x_max, x+2)
            ]
            == TileState.flagged
        )

        states = [is_bomb]

        # check if we should open more tiles
        if n_flagged == self._current_game_state[pos]:
            for _y in range(max(0, y-1) , min(y_max, y+2)):
                for _x in range(max(0, x-1), min(x_max, x+2)):
                    if (_y, _x) == (y, x):
                        continue
                    if is_flipped:
                        # only flip unflipped tiles
                        if self._current_game_state[_y, _x] == TileState.unchecked:
                            states.append(self.flip_tile((_y, _x)))
                    else:
                        states.append(self.flip_tile((_y, _x)))
        return max(states)

    def flag_tile(self, pos: Tuple[int, int]) -> None:
        if self._current_game_state[pos] == TileState.unchecked:
            self._current_game_state[pos] = TileState.flagged
        elif self._current_game_state[pos] == TileState.flagged:
            self._current_game_state[pos] = TileState.unchecked
