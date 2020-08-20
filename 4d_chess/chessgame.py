from board import Board
from tile import Tile
from piece import Piece

import tkinter as tk

class ChessGame:

    def __init__(self, corner, width, height, dimension):
        self._board = Board(dimension)
        self._root = tk.Tk()
        self._root.geometry(f"{width}x{height}+{corner[1]}+{corner[0]}")
    
    def start(self):
        self._root.mainloop()
    