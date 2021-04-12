import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from enum import Enum
import os

from numpy.lib import tile

from . import game

class TileColor(Enum):
    flagged = "#a1a1a1"
    bomb = "#fa0f0f"
    unchecked = "#a1a1a1"
    checked = "#e8e3e3"


class MineSweeperTkinter(game.MineSweeper):

    def __init__(self, height: int, width: int, bombs: int):

        super().__init__(height, width, bombs)

        self._tilesize = 20
        self._padding = 2

        self._root = tk.Tk()
        self._canvas = tk.Canvas(
            self._root, 
            width = self._width*(self._tilesize + 2*self._padding) + self._padding,
            height = self._height*(self._tilesize + 2*self._padding) + self._padding
        )
        self._canvas.pack()

        dirname = os.path.dirname(__file__)

        self._graphics = dict()

        hex2rgb = lambda s: (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16))
        def replace_color(img: Image, state: TileColor) -> Image:
            if not isinstance(img, np.ndarray):
                data = np.array(img)
            else:
                data = img
            red, green, blue = data.T # Temporarily unpack the bands for readability

            # Replace white with correct bg color
            white_areas = (red == 255) & (blue == 255) & (green == 255)
            data[...][white_areas.T] = hex2rgb(state.value)
            return Image.fromarray(data)

        # if only programming languages had a feature where you cluld loop through things

        # bomb
        bomb_image = Image.open(f"{dirname}/graphics/bomb.png")
        bomb_image = bomb_image.convert("RGB")
        self._graphics[game.TileState.bomb] = ImageTk.PhotoImage(replace_color(bomb_image, TileColor.bomb))

        # flag
        flag_image = Image.open(f"{dirname}/graphics/flag.png")
        flag_image = flag_image.convert("RGB")
        self._graphics[game.TileState.flagged] = ImageTk.PhotoImage(replace_color(flag_image, TileColor.flagged))
        
        # numbers
        numbers_image = Image.open(f"{dirname}/graphics/numbers.png")
        numbers_image_arr = np.array(numbers_image.convert("RGB"))
        for i in range(1, 9):
            self._graphics[game.TileState(i)] = ImageTk.PhotoImage(replace_color(numbers_image_arr[:, 20*(i-1):20*i, :], TileColor.checked))


        self._imagemap = np.zeros((self._shape))
        self._tilemap = np.zeros((self._shape))
        for y in range(height):
            for x in range(width):
                self._tilemap[y, x] = self._canvas.create_rectangle(
                    x * (self._tilesize + 2*self._padding) + self._padding, 
                    y * (self._tilesize + 2*self._padding) + self._padding,
                    (x+1) * (self._tilesize + 2*self._padding) + self._padding, 
                    (y+1) * (self._tilesize + 2*self._padding) + self._padding,
                    fill = TileColor.unchecked.value
                    )
        
        def on_rightclick(event):
            _x, _y = event.x, event.y

            x = _x // (self._padding*2 + self._tilesize)
            y = _y // (self._padding*2 + self._tilesize)

            self.flag_tile((y, x))
            print(self.get_tile_state((y, x)))
            refresh()
            
        
        def on_leftclick(event):
            _x, _y = event.x, event.y

            x = _x // (self._padding*2 + self._tilesize)
            y = _y // (self._padding*2 + self._tilesize)

            if self.flip_tile((y, x)):
                print("You lost")
            # delete the old and create a new rectangle
            refresh()

        def refresh():
            for y in range(self._height):
                for x in range(self._width):
                    self._canvas.delete(self._tilemap[y, x])
                    self._tilemap[y, x] = self._canvas.create_rectangle(
                        x * (self._tilesize + 2*self._padding) + self._padding, 
                            y * (self._tilesize + 2*self._padding) + self._padding,
                            (x+1) * (self._tilesize + 2*self._padding) + self._padding, 
                            (y+1) * (self._tilesize + 2*self._padding) + self._padding,
                            fill = self.tilestate_to_color(self.get_tile_state((y, x)))
                    )
                    if self._imagemap[y, x] != 0:
                        self._canvas.delete(self._imagemap[y, x])
                    if (state:= self.get_tile_state((y, x))) not in [game.TileState.unchecked, game.TileState.none]:
                        self._imagemap[y, x] = self._canvas.create_image(
                            (
                                2*self._padding + x*(2*self._padding + self._tilesize),
                                2*self._padding + y*(2*self._padding + self._tilesize)
                            ),
                            image = self._graphics[state],
                            anchor = tk.NW
                        )

        self._root.bind("<Button-1>", on_leftclick)
        self._root.bind("<Button-3>", on_rightclick)

    @staticmethod
    def tilestate_to_color(tilestate: game.TileState) -> str:
        if tilestate == game.TileState.bomb:
            return TileColor.bomb.value
        elif tilestate == game.TileState.unchecked:
            return TileColor.unchecked.value
        elif tilestate == game.TileState.flagged:
            return TileColor.flagged.value
        else:
            return TileColor.checked.value
        

    def run(self):
        self._root.mainloop()
