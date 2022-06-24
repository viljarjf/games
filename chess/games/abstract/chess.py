from chess.games.abstract.n_dim_chess import NDChess


class Chess(NDChess):
    """
    Abstract class for regular chess.

    Methods:
        move_piece: move a piece on the board and update the turn.
    """
    
    # Hard-coded dim = 2
    dimension = 2

    def __init__(self, board_size = 8, init_random: bool = False):
        
        super().__init__(self.dimension, board_size, init_random)
        
        if not init_random:
            self._board.init_2d()
