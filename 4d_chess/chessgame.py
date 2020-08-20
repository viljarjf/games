from board import Board
from tile import Tile
from piece import Piece

import tkinter as tk

class ChessGame:
    # Hard-coded dim = 4

    colors = {
        "brown": "##d87d29",
        "light_brown": "#fdc47c",
        "selected": "#90e048",
        "black": "#000000",
        "white": "#ffffff"
    }

    def __init__(self, corner, sidelength, board_size):
        self._board = Board(dimension = 4, board_size)

        self._root = tk.Tk()
        self._root.geometry(f"{sidelength}x{sidelength}+{corner[1]}+{corner[0]}")
        self._root.title("4D Chess")

        self._height = sidelength
        self._width = sidelength
        self.pad = 10
        self._tile_size = sidelength//((board_size + self.pad)*dimension + self.pad)

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
        for a in dimension:
            for b in board_size:
                for c in board_size:
                    self._canvas.create_rectangle(
                        x,
                        y,
                        x + self._tile_size,
                        y + self._tile_size,
                        fill = board_colors[index % 2]
                    )
                    index += 1
                    x += self._tile_size
                y += self._tile_size
            
            

    
    def start(self):
        self._root.mainloop()
    