import os
import tkinter as tk
from abc import ABC, abstractmethod

import numpy as np
from PIL import Image, ImageColor, ImageOps, ImageTk

from chess.games.abstract.n_dim_chess import NDChess
from chess.piece import Piece, legal_names


class NDChessGUI(NDChess, ABC):
    """nD Chess, implemented with tkinter

    Call self.start() to play.

    Args:
        corner (tuple):             (x, y) pixel coordinates for top left corner of the game
        sidelength (int):           Height and width of the game board, in pixels
        board_size (int, optional): Size of the 2D boards. In standard 2D chess, board_size = 8. 
                                    Defaults to 4.

    """
    colors = {
        "dark_tile": "#d87d29",
        "light_tile": "#fdc47c",
        "selected": "#90e048",
        "transparency": 0.8,
        "black": "#000000",
        "white": "#ffffff"
    }
    def __init__(self, corner: tuple, sidelength: int, dimension: int, board_size = 4):

        super().__init__(dimension, board_size)

        self._overlay_ids = list()
        self._previous_legal_moves = list()
        self._previous_pos = None

        # graphics
        shape = [self.board_size] * self.dimension
        self._id_board = np.array([None for n in np.zeros(shape).flatten()]).reshape(shape)
        self._root = tk.Tk()
        self._root.geometry(f"{sidelength}x{sidelength}+{corner[1]}+{corner[0]}")
        self._root.title(f"{self.dimension}D Chess")

        # pixel dimensions
        self._height = sidelength
        self._width = sidelength
        self.pad = 10
        self._tile_size = self.calc_tile_size()
        self._piece_pad = self._tile_size // 8

        # background to draw everything on
        self._canvas = tk.Canvas(
                    self._root,
                    width = self._width,
                    height = self._height
                    )
        self._canvas.pack()

        # create the transparent overlay image
        fill = ImageColor.getrgb(self.colors["selected"]) + (int(self.colors["transparency"]*255),)
        image = Image.new('RGBA', (self._tile_size, self._tile_size), fill)
        self._overlay_image = ImageTk.PhotoImage(image)

        # initialize the piece images
        self._piece_graphics = {}
        """contains imageTk.PhotoImage objects.
        key: str, piece name

        Returns:
            dict: 
                keys (str): black, white.
                vals: imageTk.PhotoImage instances
        """
        dirname = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        for p in legal_names:
            if p == "Superqueen":
                img = Image.open(f"{dirname}/graphics/Queen.png")
            else:
                img = Image.open(f"{dirname}/graphics/{p}.png")
            img_size = [self._tile_size - 2 * self._piece_pad]*2
            white_img = img.resize((img_size))
            # invert the white image to get the black ones
            black_img = ImageOps.invert(white_img.convert("RGB"))
            # color inversion does not support RGBA. 
            # Hack around this by appending the A data from the white image
            tmp = np.array(white_img)[:, :, -1]
            black_img_arr = np.array(white_img)
            black_img_arr[:, :, :-1] = np.array(black_img)
            black_img_arr[:, :, -1] = tmp
            black_img = Image.fromarray(black_img_arr)
            self._piece_graphics[p] = {"black": ImageTk.PhotoImage(black_img), 
                                       "white": ImageTk.PhotoImage(white_img)}

        def on_click(event)-> None:
            """This function runs on every click. DO NOT CALL ELSEWHERE

            Args:
                event (tkinter.Event): tkinter handles this. I don't know how or what

            Returns:
                None
            """
            x, y = event.x, event.y

            clickpos = self.pixel_to_pos(y, x)

            if clickpos is None:
                return
            
            # handle moving
            if self._previous_pos is None:
                self._previous_pos = clickpos                
                piece = self._board.get_tile(clickpos).get_piece()
                # first, ensure correct turn
                if  (piece.get_color() == "white" and self._turn) \
                    or \
                    (piece.get_color() == "black" and not self._turn):
                        self._previous_pos = None
                    
                # if colour is correct, draw an overlay of legal moves
                elif piece.get_value() is not None:
                    legal_moves = self.get_legal_moves(clickpos)
                    for pos in legal_moves:
                        y0, x0 = self.pos_to_pixels(pos) 
                        self._overlay_ids.append(self._canvas.create_image(x0, y0, image=self._overlay_image, anchor='nw'))
                    # if no overlays, then the piece cannot move.
                    if len(self._overlay_ids) == 0:
                        self._previous_pos = None

                # if the clicked tile is empty, don't store it
                else:
                    self._previous_pos = None
            else:
                self.move_piece(self._previous_pos, clickpos)
                self.draw_tile(clickpos)
                self.draw_tile(self._previous_pos)

                # regardless if the move is legal or not, delete the starting pos and legal moves
                self._previous_pos = None

                # delete the overlay of legal moves
                for id in self._overlay_ids:
                    self._canvas.delete(id)
                self._overlay_ids = []

        # we are now out of the on_click namespace
  
        # Bind the left click to the on_click function
        self._canvas.bind("<Button-1>", on_click)

        # finally, draw the board graphics
        self.draw_all(True)  


    @abstractmethod
    def calc_tile_size(self) -> int:
        """Calculate the size of each tile in pixels

        Returns:
            int
        """
        pass


    @abstractmethod
    def pos_to_pixels(self, pos: tuple) -> tuple[int, int]:
        """calculate pixel position of top-left corner of given tile position

        Args:
            pos (tuple): tile position, nD coordinates

        Returns:
            tuple[int, int]: y, x
        """
        pass


    @abstractmethod
    def pixel_to_pos(self, y: int, x: int) -> tuple:
        """Calculate position of given pixel coordinate in board coordinates
        Returns None if input is illegal

        Args:
            y (int): y pixel coordinate
            x (int): x pixel coordinate

        Returns:
            tuple: nD coordinate tuple
        """
        return None


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
            board_colors = [self.colors["dark_tile"], self.colors["light_tile"]]
            index = 0
            # the dimension is represented with the amount of for loops,
            # I don't know how to abstract it further
            # TODO replace with np.nditer maybe?
            for pos in self._board.get_iterator():
                index = sum(pos) % 2
                y, x = self.pos_to_pixels(pos)
                self._canvas.create_rectangle(
                    x,
                    y,
                    x + self._tile_size,
                    y + self._tile_size,
                    fill = board_colors[index]
                )

        # draw pieces
        for pos in self._board.get_iterator():
            p = self._board.get_tile(pos).get_piece()
            if p.get_value() is None:
                continue
            id = self._id_board[pos]
            new_id = self._draw_piece(pos, p)
            if new_id is not None:
                self._canvas.delete(id)
                self._id_board[pos] = new_id


    def draw_tile(self, pos: tuple)-> bool:
        """Redraw a single tile's piece

        Args:
            pos (tuple):    nD coordinates for the tile.

        Returns:
            bool: Success state
        """ 
        try:
            t = self._board.get_tile(pos)
            id = self._id_board[pos]
            p = t.get_piece()
            new_id = self._draw_piece(pos, p)

            self._canvas.delete(id)
            if new_id is not None:
                self._id_board[pos] = new_id
            return True
        except:
            return False


    def _draw_piece(self, pos: tuple, piece: Piece)-> int:
        """Draws the given piece to the given position. 
        Handles different piece graphics and color. 

        Args:
            pos (tuple):   nD coordinates for the tile
            piece (Piece):  The piece to draw

        Returns:
            int: tkinter canvas grapic ID. Useful for releasing memory if something else is drawn on top
        """
        color = piece.get_color()
        piece_val = piece.get_value()
        if piece_val is None:
            return None
        y, x = self.pos_to_pixels(pos)
        y += self._piece_pad
        x += self._piece_pad
        id = self._canvas.create_image((x, y), image = self._piece_graphics[piece_val][color], anchor = tk.NW)
        return id


    def toggle_click(self):
        """Toggle wether the on_click function should run on clicks
        """
        self._can_click = (not self._can_click)


    def start(self):
        """Run the game. This halts all code after the call, untill the game window is closed.
        """
        self._root.mainloop()
