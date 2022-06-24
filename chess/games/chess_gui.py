from chess.games.abstract.n_dim_chess_gui import NDChessGUI


class ChessGUI(NDChessGUI):
    """Chess, implemented with tkinter

    Call self.start() to play.

    Args:
        corner (tuple):             (x, y) pixel coordinates for top left corner of the game
        sidelength (int):           Height and width of the game board, in pixels

    """

    def __init__(self, corner: tuple, sidelength: int):

        super().__init__(corner, sidelength, dimension=2, board_size=8)

        self._board.init_2d()
        self.draw_all(True)

    # overriding abstract method
    def calc_tile_size(self) -> int:
        return (self._height - 2*self.pad)//(self.board_size)

    # overriding abstract method
    def pos_to_pixels(self, pos: tuple) -> tuple[int, int]:
        (y_i, x_i) = pos
        x = self._tile_size * x_i + self.pad
        y = self._tile_size * y_i + self.pad
        return (y, x)

    # overriding abstract method
    def pixel_to_pos(self, y: int, x: int) -> tuple:
        x_o = (x- self.pad) / (self._tile_size)
        if x_o - int(x_o) > (self._tile_size) / (self._tile_size):
            return None 
        elif x_o >= self.board_size or x_o < 0:
            return None
        x_o = int(x_o)

        y_o = (y- self.pad) / (self._tile_size)
        if y_o - int(y_o) > (self._tile_size) / (self._tile_size):
            return None
        elif y_o >= self.board_size or y_o < 0:
            return None
        y_o = int(y_o)

        return (y_o, x_o)
