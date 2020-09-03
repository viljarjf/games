from piece import Piece
import copy
import random

class Move:
    """Class for handling the available moves for a chess piece

    Args:
        dim (int): Amount of dimensions for the board
        board_size (int): Width (and height) of the 2D chess board, measured in tiles
    """

    def __init__(self, dim: int, board_size: int):
        self._dimension = dim
        self._board_size = board_size

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
            moves = self._pawn(pos, piece.get_color())
            return moves
        elif piece.get_value() == "King":
            moves = self._king(pos, piece.get_color())
            return moves
        elif piece.get_value() == "Knight":
            moves = self._knight(pos, piece.get_color())
            return moves
        elif piece.get_value() == "Rook":
            moves = self._rook(pos, piece.get_color())
            return moves
        elif piece.get_value() == "Bishop":
            moves = self._bishop(pos, piece.get_color())
            return moves
        elif piece.get_value() == "Queen":
            moves = self._queen(pos, piece.get_color())
            return moves
        elif piece.get_value() == "Superqueen":
            moves = self._superqueen(pos, piece.get_color())
            return moves

    def _pawn(self, pos: tuple, color: int)-> list:
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

    def _king(self, pos: tuple, color: int)-> list:
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

    def _knight(self, pos: tuple, color: int)-> list:
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

    def _superqueen(self, pos: tuple, color: int)-> list:
        legal_moves = []
        bound = self._board_size ** self._dimension // 5
        for p in range(random.randint(1, bound)):
            legal_moves.append(tuple([random.randint(0, 3) for d in range(self._dimension)]))
        return legal_moves

    def _rook(self, pos: tuple, color: int)-> list:
        legal_moves = []
        # loop through all dimensions
        for direcion in range(self._dimension):
            # for every dim, append all tiles in that direction
            for i in range(self._board_size):
                move = list(copy.copy(pos))
                move[direcion] = i
                legal_moves.append(tuple(move))
        return list(set(legal_moves))
    
    def _bishop(self, pos: tuple, color: int)-> list:
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
                        # range-check
                        is_legal = True
                        for x in move:
                            if x >= self._board_size or x < 0:
                                is_legal = False
                                break
                        if is_legal:
                            legal_moves.append(tuple(move))

        return list(set(legal_moves))
    def _queen(self, pos: tuple, color: int)-> list:
        # a queen is a rook and a bishop combined
        legal_moves = []
        legal_moves += self._rook(pos, color)
        legal_moves += self._bishop(pos, color)
        return list(set([tuple(move) for move in legal_moves]))