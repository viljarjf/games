from chess.games.abstract.n_dim_chess_gui import NDChessGUI

class FourDChessGUI(NDChessGUI):
    """4D Chess, implemented with tkinter

    Call self.start() to play.

    Args:
        corner (tuple):             (x, y) pixel coordinates for top left corner of the game
        sidelength (int):           Height and width of the game board, in pixels
        board_size (int, optional): Size of the 2D boards. In standard 2D chess, board_size = 8. 
                                    Defaults to 4.

    """

    def __init__(self, corner: tuple, sidelength: int, board_size = 4):

        super().__init__(corner, sidelength, dimension=4, board_size=board_size)

        self._board.init_4d()
        self.draw_all(True)

    # overriding abstract method
    def calc_tile_size(self) -> int:
        return (self._height - (self.board_size+1)*self.pad)//(self.board_size ** 2)

    # overriding abstract method
    def pos_to_pixels(self, pos: tuple) -> tuple[int, int]:
        (y_o, y_i, x_o, x_i) = pos
        x = (self.pad + self.board_size * self._tile_size) * x_o + self._tile_size * x_i + self.pad
        y = (self.pad + self.board_size * self._tile_size) * y_o + self._tile_size * y_i + self.pad
        return (y, x)

    # overriding abstract method
    def pixel_to_pos(self, y: int, x: int) -> tuple:
        x_o = (x- self.pad) / (self._tile_size * self.board_size + self.pad)
        if x_o - int(x_o) > (self._tile_size * self.board_size) / (self._tile_size * self.board_size + self.pad):
            return None 
        elif x_o >= self.board_size:
            return None
        x_o = int(x_o)

        y_o = (y- self.pad) / (self._tile_size * self.board_size + self.pad)
        if y_o - int(y_o) > (self._tile_size * self.board_size) / (self._tile_size * self.board_size + self.pad):
            return None
        elif y_o >= self.board_size:
            return None
        y_o = int(y_o)

        x_i = ((x- self.pad) % (self._tile_size * self.board_size + self.pad)) // self._tile_size
        y_i = ((y- self.pad) % (self._tile_size * self.board_size + self.pad)) // self._tile_size

        return (y_o, y_i, x_o, x_i)
