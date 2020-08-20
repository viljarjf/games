from tile import Tile
from piece import Piece

import copy
### Chess board
class Board:
    
    def __init__(self, dimension):
        self._dim = dimension

        board = [Tile()]
        for n in range(dimension):
            board = [board]*dimension
        
        self._tiles = board
    
    def get_tile(self, pos: tuple)-> Tile:
        l = copy.deepcopy(self._tiles) 
        # deep copy, we are updating l and don't want to change _tiles

        if len(pos) != self._dim:
            raise IndexError(f"Wrong axis amount in pos, \"{len(pos)}\". Must be exactly {self._dim}.")

        for n in pos:
            if n > self._dim or n < 0:
                raise IndexError("Tile position out of bounds")
            l = l[n]
        return l

