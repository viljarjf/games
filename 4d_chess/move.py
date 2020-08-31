from piece import Piece

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