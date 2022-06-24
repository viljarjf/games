from typing import Iterator, Tuple
from .tile import Tile
from .piece import Piece, legal_names

import copy
import numpy as np
import random

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
        board = [Tile() for _ in np.zeros(shape).flatten()]
        
        self._tiles = np.array(board).reshape(shape)
    
    def get_iterator(self) -> Iterator[Tuple]:
        """Returns a generator/iterator/whatever with board positions

        Returns:
            Iterator[Tuple]: each element is a tuple index
        """
        with np.nditer(
            self._tiles, 
            flags=['multi_index', "refs_ok"], 
            op_flags=['readonly']
            ) as it:
            for _ in it:
                yield it.multi_index
        
    def get_board(self) -> np.array:
        """return a copy of the array of tiles

        Returns:
            np.array
        """
        return copy.copy(self._tiles)
    
    def get_tile(self, pos: tuple)-> Tile:
        """Returns a copy of the tile in the given position

        Args:
            pos (tuple): n-D position vector to the requested tile

        Raises:
            IndexError: if the given position vector has too few dimensions, or if the vector is out of bounds      
        Returns:
            Tile: Copy of the tile at the given position
        """

        if len(pos) != self._dim:
            raise IndexError(f"Wrong axis amount in pos, \"{len(pos)}\". Must be exactly {self._dim}.")

        for n in pos:
            if n > self._size or n < 0:
                raise IndexError("Tile position out of bounds")

        return copy.copy(self._tiles[pos])
    
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
        """Move a piece from start to end. 
        Does not check wether the piece is allowed to move there according to its moveset

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

        # simple, but bad way to ensure the board is not edited if the move goes wrong.
        tmp_board = copy.deepcopy(self._tiles) 

        if(self.set_tile(end, p_start)):
            if(self.set_tile(start, Piece())):
                return True

        # this only executes if the move fails
        self._tiles = tmp_board
        return False
    
    def init_random(self):
        """Place a couple pieces randomly. Delete any previous pieces
        """
        l = legal_names[:-1] # exclude superqueen
        it = np.nditer(self._tiles, flags = ["refs_ok", "multi_index"], op_flags =["readwrite"])
        for n in it:
            if random.randint(1, 10) == 10:
                piece_val = random.choice(l)
                color = random.randint(0, 1)
                piece = Piece()
                piece.set_from_str(piece_val, color)
                self._tiles[it.multi_index].set_piece(piece)
    
    def init_4d(self):
        """Initialize the board for a standard 4x4x4x4 game
        """
        if self._dim != 4 or self._size != 4:
            raise IndexError("Board size and dimension must both be 4")
       
        for color in range(2):
            # pawns
            pawn = Piece()
            pawn.set_from_str("Pawn", color)
            start = 3*color 
            for x_o in range(4):
                for x_i in range(4):
                    self._tiles[x_o, start, x_i, 1 + color].set_piece(pawn)
        
            # the rest
            R = Piece()
            R.set_from_str("Rook", color)
            Kn = Piece()
            Kn.set_from_str("Knight", color)
            B = Piece()
            B.set_from_str("Bishop", color)
            K = Piece()
            K.set_from_str("King", color)
            Q = Piece()
            Q.set_from_str("Queen", color)
            if color:
                # white
                self._tiles[0, 3, 0, 3].set_piece(R)
                self._tiles[0, 3, 3, 3].set_piece(R)
                self._tiles[3, 3, 0, 3].set_piece(R)
                self._tiles[3, 3, 3, 3].set_piece(R)

                self._tiles[0, 3, 1, 3].set_piece(Kn)
                self._tiles[0, 3, 2, 3].set_piece(Kn)
                self._tiles[3, 3, 1, 3].set_piece(Kn)
                self._tiles[3, 3, 2, 3].set_piece(Kn)

                self._tiles[1, 3, 0, 3].set_piece(B)
                self._tiles[1, 3, 3, 3].set_piece(B)
                self._tiles[2, 3, 0, 3].set_piece(B)
                self._tiles[2, 3, 3, 3].set_piece(B)

                self._tiles[1, 3, 1, 3].set_piece(K)
                self._tiles[2, 3, 2, 3].set_piece(K)

                self._tiles[1, 3, 2, 3].set_piece(Q)
                self._tiles[2, 3, 1, 3].set_piece(Q)
            else:
                # black
                self._tiles[0, 0, 0, 0].set_piece(R)
                self._tiles[0, 0, 3, 0].set_piece(R)
                self._tiles[3, 0, 0, 0].set_piece(R)
                self._tiles[3, 0, 3, 0].set_piece(R)

                self._tiles[0, 0, 1, 0].set_piece(Kn)
                self._tiles[0, 0, 2, 0].set_piece(Kn)
                self._tiles[3, 0, 1, 0].set_piece(Kn)
                self._tiles[3, 0, 2, 0].set_piece(Kn)

                self._tiles[1, 0, 0, 0].set_piece(B)
                self._tiles[1, 0, 3, 0].set_piece(B)
                self._tiles[2, 0, 0, 0].set_piece(B)
                self._tiles[2, 0, 3, 0].set_piece(B)

                self._tiles[1, 0, 1, 0].set_piece(K)
                self._tiles[2, 0, 2, 0].set_piece(K)

                self._tiles[1, 0, 2, 0].set_piece(Q)
                self._tiles[2, 0, 1, 0].set_piece(Q)

        # [R, Kn, T, R], [B, K, Q, B], [B, Q, K, B], [R, T, Kn, R]


    def init_2d(self):
        """Initialize the board for a standard game
        """
        if self._dim != 2 or self._size != 8:
            raise IndexError("Board size must be 8 and dimension must be 2")
       
        # pawns
        pawn = Piece()
        pawn.set_from_str("Pawn", 0)
        for x in range(8):
            self._tiles[1, x].set_piece(pawn)
        # pawns
        pawn = Piece()
        pawn.set_from_str("Pawn", 1)
        for x in range(8):
            self._tiles[6, x].set_piece(pawn)
        
        # the rest
        R = Piece()
        R.set_from_str("Rook", 1)
        Kn = Piece()
        Kn.set_from_str("Knight", 1)
        B = Piece()
        B.set_from_str("Bishop", 1)
        K = Piece()
        K.set_from_str("King", 1)
        Q = Piece()
        Q.set_from_str("Queen", 1)
        # white
        self._tiles[7, 7].set_piece(R)
        self._tiles[7, 6].set_piece(Kn)
        self._tiles[7, 5].set_piece(B)
        self._tiles[7, 4].set_piece(Q)
        self._tiles[7, 3].set_piece(K)
        self._tiles[7, 2].set_piece(B)
        self._tiles[7, 1].set_piece(Kn)
        self._tiles[7, 0].set_piece(R)

        #black
        R = Piece()
        R.set_from_str("Rook", 0)
        Kn = Piece()
        Kn.set_from_str("Knight", 0)
        B = Piece()
        B.set_from_str("Bishop", 0)
        K = Piece()
        K.set_from_str("King", 0)
        Q = Piece()
        Q.set_from_str("Queen", 0)
        # white
        self._tiles[0, 7].set_piece(R)
        self._tiles[0, 6].set_piece(Kn)
        self._tiles[0, 5].set_piece(B)
        self._tiles[0, 4].set_piece(Q)
        self._tiles[0, 3].set_piece(K)
        self._tiles[0, 2].set_piece(B)
        self._tiles[0, 1].set_piece(Kn)
        self._tiles[0, 0].set_piece(R)

    def __str__(self):
        if self._dim != 2:
            return self
        line = "+----" * 8 + "+\n"
        row = "| {} " * 8 + "|\n"
        board = (line + row) * 8 + line
        return board.format(*[self._tiles[pos] for pos in self.get_iterator()])
