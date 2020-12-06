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
        self._mover = Mover(self)

        shape = [self._size] * self._dim
        board = [Tile() for n in np.zeros(shape).flatten()]
        
        self._tiles = np.array(board).reshape(shape)
    
    def get_legal_moves(self, pos)-> list:
        p = self.get_tile(pos).get_piece()
        return self._mover.get_legal_moves(p, pos)

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
                # update the mover if the board changed
                self._mover = Mover(self)
                return True

        # this only executes if the move fails
        self._tiles = tmp_board
        del tmp_board # release the memory
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


class Mover:
    """Class for handling the available moves for a chess piece

    Args:
        dim (int): Amount of dimensions for the board
        board_size (int): Width (and height) of the 2D chess board, measured in tiles
    """

    def __init__(self, board: Board):
        self._board = board
        self._dimension = board._dim
        self._board_size = board._size


    def get_legal_moves(self, piece: Piece, pos: tuple)-> list:
        """Get a list of all legal moves for a piece, given the dimensions and board size
        Note: Does not take other pieces into account

        Args:
            piece (Piece): The piece to get moves for
            pos (tuple): The position vector for the piece

        Returns:
            list: list of tuples (position vectors) of legal moves
        """
        if piece.get_value() == "Pawn":
            moves = self._pawn(pos)
            return moves
        elif piece.get_value() == "King":
            moves = self._king(pos)
            return moves
        elif piece.get_value() == "Knight":
            moves = self._knight(pos)
            return moves
        elif piece.get_value() == "Rook":
            moves = self._rook(pos)
            return moves
        elif piece.get_value() == "Bishop":
            moves = self._bishop(pos)
            return moves
        elif piece.get_value() == "Queen":
            moves = self._queen(pos)
            return moves
        elif piece.get_value() == "Trebuchet":
            moves = self._trebuchet(pos)
            return moves
        elif piece.get_value() == "Superqueen":
            moves = self._superqueen(pos)
            return moves
    

    def _pawn(self, pos: tuple)-> list:
        # VERY WRONG, only for testing
        legal_moves = []
        for a in range(-1, 2):
            for b in range(-1, 2):
                for c in range(-1, 2):
                    for d in range(-1, 2):
                        x1 = pos[0]+a if (pos[0]+a >= 0 and pos[0]+a < self._dimension) else None
                        x2 = pos[1]+b if (pos[1]+b >= 0 and pos[1]+b < self._dimension) else None
                        x3 = pos[2]+c if (pos[2]+c >= 0 and pos[2]+c < self._board_size) else None
                        x4 = pos[3]+d if (pos[3]+d >= 0 and pos[3]+d < self._board_size) else None
                        move = (x1, x2, x3, x4)
                        if None in move:
                            continue
                        legal_moves.append(move)
        return legal_moves


    def _king(self, pos: tuple)-> list:
        legal_moves = []
        # outer loop sets up +/- 1 for each dimension, but only for one dim at a time
        for d in range(self._dimension):
            for i_1, p_1 in enumerate(pos):
                if p_1+1 < self._board_size:
                    # changed to list, to enable item assignment
                    move = list(copy.copy(pos))
                    move[i_1] += 1
                    # inner loop does the same as outer loop, but skips the dimension already used
                    for i_2, p_2 in enumerate(move):
                        if i_2 == i_1:
                            continue
                        if p_2+1 < self._board_size:
                            finalmove = copy.copy(move)
                            finalmove[i_2] += 1
                            # change back to tuple, so we can remove dulpicates in the end
                            legal_moves.append(tuple(finalmove))
                        if p_2-1 > -1:
                            finalmove = copy.copy(move)
                            finalmove[i_2] -= 1
                            legal_moves.append(tuple(finalmove))
                    # also add the case of only choosing one dim
                    legal_moves.append(tuple(move))
                if p_1-1 > -1:
                    move = list(copy.copy(pos))
                    move[i_1] -= 1
                    for i_2, p_2 in enumerate(move):
                        if i_2 == i_1:
                            continue
                        if p_2+1 < self._board_size:
                            finalmove = copy.copy(move)
                            finalmove[i_2] += 1
                            legal_moves.append(tuple(finalmove))
                        if p_2-1 > -1:
                            finalmove = copy.copy(move)
                            finalmove[i_2] -= 1
                            legal_moves.append(tuple(finalmove))
                    legal_moves.append(tuple(move))
                # remove duplicates. This keeps the overlay from turning opaque when a tile has many possible ways to get to
        return list(set(legal_moves))


    def _knight(self, pos: tuple)-> list:
        legal_moves = []
        for d in range(self._dimension):
            for i_1, p_1 in enumerate(pos):
                    if p_1+2 < self._board_size:
                        # changed to list, to enable item assignment
                        move = list(copy.copy(pos))
                        move[i_1] += 2
                        # inner loop does the same as outer loop, but skips the dimension already used
                        for i_2, p_2 in enumerate(move):
                            if i_2 == i_1:
                                continue
                            if p_2+1 < self._board_size:
                                finalmove = copy.copy(move)
                                finalmove[i_2] += 1
                                # change back to tuple, so we can remove dulpicates in the end
                                legal_moves.append(tuple(finalmove))
                            if p_2-1 > -1:
                                finalmove = copy.copy(move)
                                finalmove[i_2] -= 1
                                legal_moves.append(tuple(finalmove))
                    if p_1-2 > -1:
                        move = list(copy.copy(pos))
                        move[i_1] -= 2
                        for i_2, p_2 in enumerate(move):
                            if i_2 == i_1:
                                continue
                            if p_2+1 < self._board_size:
                                finalmove = copy.copy(move)
                                finalmove[i_2] += 1
                                legal_moves.append(tuple(finalmove))
                            if p_2-1 > -1:
                                finalmove = copy.copy(move)
                                finalmove[i_2] -= 1
                                legal_moves.append(tuple(finalmove))
                # remove duplicates. This keeps the overlay from turning opaque when a tile has many possible ways to get to
        return list(set(legal_moves))


    def _superqueen(self, pos: tuple)-> list:
        legal_moves = []
        bound = self._board_size ** self._dimension // 5
        for p in range(random.randint(1, bound)):
            legal_moves.append(tuple([random.randint(0, 3) for d in range(self._dimension)]))
        return legal_moves


    def _rook(self, pos: tuple)-> list:
        legal_moves = []
        # loop through all dimensions
        for direcion in range(self._dimension):
            # for every dim, append all tiles in that direction
            for i in range(self._board_size):
                move = list(copy.copy(pos))
                move[direcion] = i
                # skip starting pos
                if tuple(move) == pos:
                    continue
                legal_moves.append(tuple(move))

        return list(set(legal_moves))


    def _bishop(self, pos: tuple)-> list:
        legal_moves = []
        # first, set up a loop over two dimensions at a time
        for dim in range(self._dimension):
            for index in range(self._dimension):
                if index == dim: 
                    continue
                # then, add all moves with those two dimensions + n for n < _board_size
                # actually, loop from -board size to board_size, but remove illegal positions
                # also loop the sign of one of the dimensions, to get both diagonals
                for sign in range(-1, 2, 2):
                    for n in range(-self._board_size, self._board_size):
                        move = list(copy.copy(pos))
                        move[dim] += n
                        move[index] += n * sign
                        
                        # remove the starting position
                        if tuple(move) == pos:
                            continue
                        # range-check
                        is_legal = True
                        for x in move:
                            if x >= self._board_size or x < 0:
                                is_legal = False
                                break
                        if is_legal:
                            legal_moves.append(tuple(move))

        return list(set(legal_moves))


    def _queen(self, pos: tuple)-> list:
        # a queen is a rook and a bishop combined
        legal_moves = []
        legal_moves += self._rook(pos)
        legal_moves += self._bishop(pos)
        return list(set([tuple(move) for move in legal_moves]))
    

    def _trebuchet(self, pos: tuple)-> list:
        # add (3, 1, 1, 0) in random order
        legal_moves = []
        for d in range(self._dimension):
            for sign_1 in range(-3, 4, 6):
                for i_1, p_1 in enumerate(pos):
                    if p_1 + sign_1 < self._board_size and p_1 + sign_1 > -1:
                        # changed to list, to enable item assignment
                        move = list(copy.copy(pos))
                        move[i_1] += sign_1
                        legal_moves.append(tuple(move))
                        for sign_2 in range(-1, 2, 2):
                            for i_2, p_2 in enumerate(move):
                                # remove the tile one closer to the starting tile
                                if i_1 == i_2 and abs(sign_2)/sign_2 != abs(sign_1)/sign_1:
                                    continue
                                if p_2 + sign_2 < self._board_size and p_2 + sign_2 > -1:
                                    move_2 = copy.copy(move)
                                    move_2[i_2] += sign_2
                                    legal_moves.append(tuple(move_2))
                                    for sign_3 in range(-1, 2, 2):
                                        for i_3, p_3 in enumerate(move_2):
                                            if i_3 == i_1 and abs(sign_3)/sign_3 != abs(sign_1)/sign_1:
                                                continue
                                            elif i_3 == i_2:
                                                continue
                                            if p_3 + sign_3 < self._board_size and p_3 + sign_3 > -1:
                                                move_3 = copy.copy(move_2)
                                                move_3[i_3] += sign_3
                                                legal_moves.append(tuple(move_3))

        # remove duplicates. This keeps the overlay from turning opaque when a tile has many possible ways to get to
        return list(set(legal_moves))