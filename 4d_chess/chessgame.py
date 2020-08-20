from board import Board
from tile import Tile
from piece import Piece

import tkinter as tk

class ChessGame:

    colors = {
        "brown": "##d87d29",
        "light_brown": "#fdc47c",
        "selected": "#90e048",
        "black": "#000000",
        "white": "#ffffff"
    }

    def __init__(self, corner, sidelength, dimension, board_size):
        self._board = Board(dimension)

        self._root = tk.Tk()
        self._root.geometry(f"{sidelength}x{sidelength}+{corner[1]}+{corner[0]}")
        self._root.title(f"{dimension}D Chess")

    
    def start(self):
        self._root.mainloop()
    