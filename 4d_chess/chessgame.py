from board import Board
from tile import Tile
from piece import Piece

import tkinter as tk

class ChessGame:
    # Hard-coded dim = 4

    colors = {
        "brown": "#d87d29",
        "light_brown": "#fdc47c",
        "selected": "#90e048",
        "black": "#000000",
        "white": "#ffffff"
    }
    dimension = 4

    def __init__(self, corner, sidelength, board_size):
        self._board = Board(dimension = self.dimension, board_size = board_size)
        self._can_click = True

        self._root = tk.Tk()
        self._root.geometry(f"{sidelength}x{sidelength}+{corner[1]}+{corner[0]}")
        self._root.title("4D Chess")

        self._height = sidelength
        self._width = sidelength
        self.pad = 10
        self._tile_size = (sidelength - (self.dimension+1)*self.pad)//(self.dimension*board_size)

        self._canvas = tk.Canvas(
                    self._root,
                    width = self._width,
                    height = self._height
                    )
        self._canvas.pack()

        x = self.pad
        y = self.pad
        board_colors = [self.colors["brown"], self.colors["light_brown"]]
        index = 0

        for a in range(self.dimension):
            for b in range(self.dimension):
                for c in range(board_size):
                    for d in range(board_size):
                        self._canvas.create_rectangle(
                            x,
                            y,
                            x + self._tile_size,
                            y + self._tile_size,
                            fill = board_colors[index]
                        )
                        index += 1
                        index %= 2
                        x += self._tile_size
                    index += 1
                    index %= 2
                    x -= self._tile_size * board_size
                    y += self._tile_size
                index += 1
                index %= 2
                x += self._tile_size * board_size + self.pad
                y -= self._tile_size * board_size
            index += 1
            index %= 2
            y += self._tile_size * board_size + self.pad
            x = self.pad

        def on_click(event)-> None:
            x, y = event.x, event.y

            x_o = (x- self.pad) / (self._tile_size * board_size + self.pad)
            if x_o - int(x_o) > (self._tile_size * board_size) / (self._tile_size * board_size + self.pad):
                return None
            elif x_o >= self.dimension:
                return None
            x_o = int(x_o)

            y_o = (y- self.pad) / (self._tile_size * board_size + self.pad)
            if y_o - int(y_o) > (self._tile_size * board_size) / (self._tile_size * board_size + self.pad):
                return None
            elif y_o >= self.dimension:
                return None
            y_o = int(y_o)

            x_i = ((x- self.pad) % (self._tile_size * board_size + self.pad)) // self._tile_size

            y_i = ((y- self.pad) % (self._tile_size * board_size + self.pad)) // self._tile_size

            print(x_o, y_o, x_i, y_i)

        self._canvas.bind("<Button-1>", on_click)

    def toggle_click(self):
        self._can_click = (not self._can_click)

    def start(self):

        self._root.mainloop()
    