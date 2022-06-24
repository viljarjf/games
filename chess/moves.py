from .piece import Piece

import copy
import random
import itertools

class Moves:
    """Class for handling the available moves for a chess piece

    Args:
        dim (int): Amount of dimensions for the board
        board_size (int): Width (and height) of the 2D chess board, measured in tiles
    """

    def __init__(self, dim: int, board_size: int):
        self._dimension = dim
        self._board_size = board_size

    def get_moves(self, piece: Piece, pos: tuple)-> list[list[tuple]]:
        """Get a list of all legal moves for a piece, given the dimensions and board size
        Note: Does not take other pieces into account

        Args:
            piece (Piece): The piece to get moves for
            pos (tuple): The position vector for the piece

        Returns:
            list: 
                each element is a list of tuples (position vectors) of legal moves.
                each list is a direction from the piece.
        """
        if piece.get_value() == "Pawn":
            moves = self._pawn(pos, piece.get_color())
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

    def _pawn(self, pos: tuple, color: str)-> list[list[tuple]]:
        if self._dimension == 4:
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
            return [legal_moves]
        elif self._dimension == 2:
            legal_moves = []
            up_or_down = 1 if color == "black" else -1
            row = 1 if color == "black" else 6
            if pos[0] == row:
                legal_moves.append(self._get_moves_in_dir(pos, [up_or_down, 0])[0:2])
            else:
                legal_moves.append(self._get_moves_in_dir(pos, [up_or_down, 0])[0:1])
            for dir in [[up_or_down, -1], [up_or_down, 1]]:
                legal_moves.append(self._get_moves_in_dir(pos, dir)[0:1])
            return legal_moves

    def _king(self, pos: tuple)-> list[list[tuple]]:
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
        return list([move] for move in set(legal_moves))

    def _knight(self, pos: tuple)-> list[list[tuple]]:
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
        
        return list([move] for move in set(legal_moves))
        

    def _superqueen(self, pos: tuple)-> list[list[tuple]]:
        legal_moves = []
        bound = self._board_size ** self._dimension // 5
        for p in range(random.randint(1, bound)):
            legal_moves.append(tuple([random.randint(0, 3) for d in range(self._dimension)]))
        return list([move] for move in set(legal_moves))
        
    def _get_moves_in_dir(self, pos: tuple, dir: tuple) -> list[tuple]:
        moves = []
        # max board_size iterations necessary
        for n in range(1, self._board_size):
            move = tuple(i + j*n for i, j in zip(pos, dir))
            if any(i < 0 or i >= self._board_size for i in move):
                break
            moves.append(move)
        return moves

    def _rook(self, pos: tuple)-> list[list[tuple]]:
        legal_moves = []
        directions = list(set([
            *itertools.permutations([1] + [0]*(self._dimension - 1)),
            *itertools.permutations([-1] + [0]*(self._dimension - 1))
        ]))
        for direction in directions:
            legal_moves.append(self._get_moves_in_dir(pos, direction))

        return legal_moves

    def _bishop(self, pos: tuple)-> list[list[tuple]]:
        legal_moves = []
        directions = list(set([
            *itertools.permutations([1, 1] + [0]*(self._dimension - 2)),
            *itertools.permutations([-1, 1] + [0]*(self._dimension - 2)),
            *itertools.permutations([-1, -1] + [0]*(self._dimension - 2)),
        ]))
        for direction in directions:
            legal_moves.append(self._get_moves_in_dir(pos, direction))

        return legal_moves

    def _queen(self, pos: tuple)-> list[list[tuple]]:
        # a queen is a rook and a bishop combined
        legal_moves = []
        legal_moves += self._rook(pos)
        legal_moves += self._bishop(pos)
        return legal_moves
    
    def _trebuchet(self, pos: tuple)-> list[list[tuple]]:
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
        return [list(set(legal_moves))]