from piece import Piece
import copy
import random

_dimension = None
_board_size = None

def set_vars(dim: int, board_size: int)-> None:
    global _dimension
    global _board_size
    _dimension = dim
    _board_size = board_size

def get_legal_moves(piece: Piece, pos: tuple)-> list:
    if _dimension is None or _board_size is None:
        raise Exception("Dimension and board size not set. Please do so with move.set_vars")
    if piece.get_value() == "Pawn":
        moves = _pawn(pos, piece.get_color())
        return moves
    elif piece.get_value() == "King":
        moves = _king(pos, piece.get_color())
        return moves
    elif piece.get_value() == "Knight":
        moves = _knight(pos, piece.get_color())
        return moves
    elif piece.get_value() == "Rook":
        moves = _rook(pos, piece.get_color())
        return moves
    elif piece.get_value() == "SuperQueen":
        moves = _superqueen(pos, piece.get_color())
        return moves

def _pawn(pos: tuple, color: int)-> list:
    # VERY WRONG, only for testing
    legal_moves = []
    for a in range(-1, 2):
        for b in range(-1, 2):
            for c in range(-1, 2):
                for d in range(-1, 2):
                    x1 = pos[0]+a if (pos[0]+a >= 0 and pos[0]+a < _dimension) else None
                    x2 = pos[1]+b if (pos[1]+b >= 0 and pos[1]+b < _dimension) else None
                    x3 = pos[2]+c if (pos[2]+c >= 0 and pos[2]+c < _board_size) else None
                    x4 = pos[3]+d if (pos[3]+d >= 0 and pos[3]+d < _board_size) else None
                    move = (x1, x2, x3, x4)
                    if None in move:
                        continue
                    legal_moves.append(move)
    return legal_moves

def _king(pos: tuple, color: int)-> list:
    legal_moves = []
    # outer loop sets up +/- 1 for each dimension, but only for one dim at a time
    for d in range(_dimension):
        for i_1, p_1 in enumerate(pos):
            if p_1+1 < _dimension:
                # changed to list, to enable item assignment
                move = list(copy.copy(pos))
                move[i_1] += 1
                # inner loop does the same as outer loop, but skips the dimension already used
                for i_2, p_2 in enumerate(move):
                    if i_2 == i_1:
                        continue
                    if p_2+1 < _dimension:
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
                    if p_2+1 < _dimension:
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

def _knight(pos: tuple, color: int)-> list:
    legal_moves = []
    for d in range(_dimension):
        for i_1, p_1 in enumerate(pos):
                if p_1+2 < _dimension:
                    # changed to list, to enable item assignment
                    move = list(copy.copy(pos))
                    move[i_1] += 2
                    # inner loop does the same as outer loop, but skips the dimension already used
                    for i_2, p_2 in enumerate(move):
                        if i_2 == i_1:
                            continue
                        if p_2+1 < _dimension:
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
                        if p_2+1 < _dimension:
                            finalmove = copy.copy(move)
                            finalmove[i_2] += 1
                            legal_moves.append(tuple(finalmove))
                        if p_2-1 > -1:
                            finalmove = copy.copy(move)
                            finalmove[i_2] -= 1
                            legal_moves.append(tuple(finalmove))
            # remove duplicates. This keeps the overlay from turning opaque when a tile has many possible ways to get to
    return list(set(legal_moves))

def _superqueen(pos: tuple, color: int)-> list:
    legal_moves = []
    for p in range(random.randint(1, 20)):
        legal_moves.append(tuple([random.randint(0, 3) for d in range(_dimension)]))
    return legal_moves

def _rook(pos: tuple, color: int)-> list:
    legal_moves = []
    # loop through all dimensions
    for direcion in range(_dimension):
        # for every dim, append all tiles in that direction
        for i in range(_board_size):
            move = list(copy.copy(pos))
            move[direcion] = i
            legal_moves.append(tuple(move))
    return list(set(legal_moves))