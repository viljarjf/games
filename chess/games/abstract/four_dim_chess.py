from chess.games.abstract.n_dim_chess import NDChess


class FourDimChess(NDChess):
    """
    Abstract class for 4D chess.

    Methods:
        move_piece: move a piece on the board and update the turn.
    """
    
    # Hard-coded dim = 4
    dimension = 4

    def __init__(self, board_size = 4, init_random: bool = False):
        
        super().__init__(self.dimension, board_size, init_random)
        
        if not init_random:
            self._board.init_4d()
