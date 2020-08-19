from tile import Tile
from piece import Piece
### Chess board
class Board:
    
    def __init__(self, dimension):
        self._dim = dimension

        board = [Tile()]
        for n in range(dimension):
            board = [board]*dimension
        
        self._tiles = board

        