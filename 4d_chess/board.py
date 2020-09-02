from tile import Tile
from piece import Piece

import copy
import numpy as np
### Chess board
class Board:
    """Chess board class. 

    Args:
        dimension (int):  Amount of dimensions to use. 
                          dimension = 4 is the only value currently tested, but other values might work
        board_size (int): Size of the 2D board(s) measured in tiles. 
                          Standard 2D chess has board_size = 8. Only 4 has been tested
    """
    
    def __init__(self, dimension, board_size):
        self._dim = dimension
        self._size = board_size

        shape = [self._size] * self._dim
        board = [Tile() for n in np.zeros(shape).flatten()]

        
        self._tiles = np.array(board).reshape(shape)
    
    def get_tile(self, pos: tuple)-> Tile:
        """Returns a copy of the tile in the given position

        Args:
            pos (tuple): n-D position vector to the requested tile

        Raises:
            IndexError: if the given position vector has too few dimensions, or if the vector is out of bounds      
        Returns:
            Tile: Copy of the tile at the given position
        """
        l = copy.deepcopy(self._tiles) 
        # deep copy, we are updating l and don't want to change _tiles

        if len(pos) != self._dim:
            raise IndexError(f"Wrong axis amount in pos, \"{len(pos)}\". Must be exactly {self._dim}.")

        for n in pos:
            if n > self._size or n < 0:
                raise IndexError("Tile position out of bounds")

        return l[pos]
    
    def set_tile(self, pos: tuple, piece: Piece)-> bool:
        """Set a tile to contain a new piece

        Args:
            pos (tuple): Position to update.
            piece (Piece): The piece to put in the tile

        Returns:
            bool: Success state of the function
        """
        try:
            # check if the position is valid
            self.get_tile(pos)

            self._tiles[pos].set_piece(piece)
            return True
        except:
            return False

    def move(self, start: tuple, end: tuple)-> bool:
        """Move a piece from start to end. Does not check wether the piece is allowed to move there.

        Args:
            start (tuple): start position 
            end (tuple): destination position

        Returns:
            bool: Success or failure of the move
        """
        p_start = self.get_tile(start).get_piece()
        p_end = self.get_tile(end).get_piece()
    
        # start is empty
        if p_start.get_color() == None:
            return False

        # same team
        if  p_start.get_color() == p_end.get_color():
            return False

        tmp_board = copy.deepcopy(self._tiles) 

        if(self.set_tile(end, p_start)):
            if(self.set_tile(start, Piece())):
                return True

        # this only executes if the move fails
        self._tiles = tmp_board
        return False