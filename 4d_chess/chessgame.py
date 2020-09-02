from board import Board
from tile import Tile
from piece import Piece
from move import Move

import tkinter as tk
import numpy as np
from PIL import Image, ImageTk, ImageColor

class FourDimChess:
    """4D Chess

    Call self.start() to play.

    Args:
        corner (tuple): (x, y) pixel coordinates for top left corner of the game
        sidelength (int): Height and width of the game board, in pixels

    """
    
    colors = {
        "brown": "#d87d29",
        "light_brown": "#fdc47c",
        "selected": "#90e048",
        "transparency": 0.7,
        "black": "#000000",
        "white": "#ffffff"
    }
    # Hard-coded dim = 4
    dimension = 4
    board_size = 4

    def __init__(self, corner, sidelength):
        self._board = Board(dimension = self.dimension, board_size = self.board_size)
        self._can_click = True
        self._turn = 1
        self._overlay_ids = []
        self._move = Move(self.dimension, self.board_size)

        shape = [self.board_size] * self.dimension
        self._id_board = np.array([None for n in np.zeros(shape).flatten()]).reshape(shape)

        self._root = tk.Tk()
        self._root.geometry(f"{sidelength}x{sidelength}+{corner[1]}+{corner[0]}")
        self._root.title("4D Chess")

        self._height = sidelength
        self._width = sidelength
        self.pad = 10
        self._piece_pad = 10
        self._tile_size = (sidelength - (self.dimension+1)*self.pad)//(self.dimension*self.board_size)

        self._canvas = tk.Canvas(
                    self._root,
                    width = self._width,
                    height = self._height
                    )
        self._canvas.pack()


        fill = ImageColor.getrgb(self.colors["selected"]) + (int(self.colors["transparency"]*255),)
        image = Image.new('RGBA', (self._tile_size, self._tile_size), fill)
        self._overlay_image = ImageTk.PhotoImage(image)

        self.draw_all(redraw = True)
                        

        def on_click(event)-> None:
            """This function runs on every click. DO NOT CALL ELSEWHERE

            At the testing stage, this creates a piece on the selected tile, draws it, and shows all possible moves.
            When complete, this should handle all logic for moving pieces

            Args:
                event (tkinter.Event): tkinter handles this. I don't know how or what

            Returns:
                None
            """
            x, y = event.x, event.y

            for id in self._overlay_ids:
                self._canvas.delete(id)

            x_o = (x- self.pad) / (self._tile_size * self.board_size + self.pad)
            if x_o - int(x_o) > (self._tile_size * self.board_size) / (self._tile_size * self.board_size + self.pad):
                return None
            elif x_o >= self.dimension:
                return None
            x_o = int(x_o)

            y_o = (y- self.pad) / (self._tile_size * self.board_size + self.pad)
            if y_o - int(y_o) > (self._tile_size * self.board_size) / (self._tile_size * self.board_size + self.pad):
                return None
            elif y_o >= self.dimension:
                return None
            y_o = int(y_o)

            x_i = ((x- self.pad) % (self._tile_size * self.board_size + self.pad)) // self._tile_size

            y_i = ((y- self.pad) % (self._tile_size * self.board_size + self.pad)) // self._tile_size
            
            clickpos = (x_o, y_o, x_i, y_i)
            piece = Piece()
            piece.set_from_str("Queen", self._turn)
            if self._board.set_tile(clickpos, piece):
                if(self.draw_tile(clickpos)):
                    self._turn += 1
                    self._turn %= 2

            cur_piece = self._board.get_tile(clickpos).get_piece()
            legal_moves = self._move.get_legal_moves(cur_piece, clickpos)       
            
            for pos in legal_moves:
                y0, x0 = self.pixel_from_pos(pos) 
                self._overlay_ids.append(self._canvas.create_image(x0, y0, image=self._overlay_image, anchor='nw'))
            
        # Bind the left click to the on_click function
        self._canvas.bind("<Button-1>", on_click)
    
    def draw_all(self, redraw = False):
        """ 
        Draw the tiles and pieces on the board

        Args:
            redraw (bool, optional): Delete all graphics from memory and redraw them. Defaults to False.
        """
        if redraw:
            self._canvas.delete("all")
            # draw tiles
            x = self.pad
            y = self.pad
            board_colors = [self.colors["brown"], self.colors["light_brown"]]
            index = 0
            for a in range(self.dimension):
                for b in range(self.dimension):
                    for c in range(self.board_size):
                        for d in range(self.board_size):
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
                        x -= self._tile_size * self.board_size
                        y += self._tile_size
                    index += 1
                    index %= 2
                    x += self._tile_size * self.board_size + self.pad
                    y -= self._tile_size * self.board_size
                index += 1
                index %= 2
                y += self._tile_size * self.board_size + self.pad
                x = self.pad

        # draw pieces
        for x_o in range(self.dimension):
            for y_o in range(self.dimension):
                for x_i in range(self.board_size):
                    for y_i in range(self.board_size):
                        pos = (x_o, y_o, x_i, y_i)
                        p = self._board.get_tile(pos).get_piece()
                        if p.get_value() is None:
                            continue
                        c = p.get_color()
                        p = None
                        y, x = self.pixel_from_pos(pos)
                        x += 2 * self._piece_pad
                        y += 2 * self._piece_pad
                        self._canvas.create_oval(
                            x,
                            y,
                            x + self._tile_size - 2 *self._piece_pad,
                            y + self._tile_size - 2 *self._piece_pad,
                            fill = self.colors[c]
                        )
    
    def draw_tile(self, pos)-> bool:
        """Redraw a single tile's piece

        Args:
            pos (tuple):    (x_o, y_o, x_i, y_i), 4D coordinates for the tile. 
                            o-subscript refers to "outer", meaning position of the boards
                            i_subscript refers to "inner", meaning position on a single 2D board 

        Returns:
            bool: Success state
        """ 
        t = self._board.get_tile(pos)
        try:
            id = self._id_board[pos]
            self._canvas.delete(id)
        finally:
            p = t.get_piece()
            if p.get_value() is None:
                return False
            c = p.get_color()
            p = None
            y, x = self.pixel_from_pos(pos)
            x += self._piece_pad
            y += self._piece_pad
            self._id_board[pos] = self._canvas.create_oval(
                x,
                y,
                x + self._tile_size - 2 * self._piece_pad,
                y + self._tile_size - 2 * self._piece_pad,
                fill = self.colors[c]
            )
            return True
    
    def pixel_from_pos(self, pos)-> tuple:
        """Get 2D pixel coordinates from 4D position.
        Specifically, get the (y, x) coordinates of the top left corner of the tile

        Args:
            pos (tuple):    (x_o, y_o, x_i, y_i), 4D coordinates for the tile. 
                            o-subscript refers to "outer", meaning position of the boards
                            i_subscript refers to "inner", meaning position on a single 2D board

        Returns:
            tuple: (y, x), pixel coordinates of top left corner to the position
        """
        (x_o, y_o, x_i, y_i) = pos
        x = (self.pad + self.board_size * self._tile_size) * x_o + self._tile_size * x_i + self.pad
        y = (self.pad + self.board_size * self._tile_size) * y_o + self._tile_size * y_i + self.pad
        return (y, x)

    def toggle_click(self):
        """Toggle wether the on_click function should run on clicks
        """
        self._can_click = (not self._can_click)

    def start(self):
        """Run the game. This halts all code after the call, untill the game window is closed.
        """
        self._root.mainloop()

    