import numpy as np
import tkinter as tk


# I don't like python's enum
class tile:
    EMPTY = 0
    YELLOW = 1
    RED = 2

COLORS = {
    tile.EMPTY  : "#399ad5",
    tile.YELLOW : "#aaaa00",
    tile.RED    : "#ff0000",
}


class FourInARowGui(tk.Tk):

    padding_px = 10

    def __init__(
        self,
        game_width: int,
        game_height: int,
        window_width: int = 700,
        window_height: int = 500,
        **tk_kwargs
    ) -> None:
        super().__init__(**tk_kwargs)

        self.turn = 0
        self.game_size = (self.game_height, self.game_width) = game_height, game_width
        self.board = np.full(self.game_size, tile.EMPTY)
        self.tilemap = np.empty(self.game_size, dtype=int)

        self.canvas = tk.Canvas(
            self,
            width=window_width,
            height=window_height,
        )
        self.canvas.pack()

        self._update_tile_sizes(window_width, window_height)

        for y in range(self.game_height):
            for x in range(self.game_width):
                xpos = self.padding_px + x * (self.tilesize_px + self.padding_px)
                ypos = self.padding_px + y * (self.tilesize_px + self.padding_px)
                self.tilemap[y, x] = self.canvas.create_rectangle(
                    xpos,
                    ypos,
                    xpos + self.tilesize_px,
                    ypos + self.tilesize_px,
                    fill=COLORS[tile.EMPTY],
                )
        self.update()
        self.window_width = self.winfo_width()
        self.window_height = self.winfo_height()
        self.bind("<Configure>", self._resize_handler)
        self.bind("<Button-1>", self._click_handler)
    
    def lock(self):
        self.bind("<Button-1>", lambda event: None)
    
    def _update_tile_sizes(self, window_width: int, window_height: int):
        num_tiles_width = self.game_width
        num_pad_width = num_tiles_width + 1
        tilesize_px_width = (window_width - num_pad_width * self.padding_px) // num_tiles_width

        num_tiles_height = self.game_height
        num_pad_height = num_tiles_height + 1
        tilesize_px_height = (window_height - num_pad_height * self.padding_px) // num_tiles_height

        self.tilesize_px = min(tilesize_px_height, tilesize_px_width)

    def _resize_canvas(self, width: int, height: int):
        self.canvas.config(width=width, height=height)

    def _redraw(self):
        for y in range(self.game_height):
            for x in range(self.game_width):
                xpos = self.padding_px + x * (self.tilesize_px + self.padding_px)
                ypos = self.padding_px + y * (self.tilesize_px + self.padding_px)
                self.canvas.coords(
                    self.tilemap[y, x],
                    xpos,
                    ypos,
                    xpos + self.tilesize_px,
                    ypos + self.tilesize_px,
                )
                self.canvas.itemconfigure(
                    self.tilemap[y, x],
                    fill=COLORS[self.board[y, x]],
                )
        self.update()

    def _resize_handler(self, event: tk.Event):
        if event.width != self.window_width or event.height != self.window_height:
            self.window_width = event.width
            self.window_height = event.height
            self._update_tile_sizes(event.width, event.height)
            self._resize_canvas(event.width, event.height)
            self._redraw()
    
    def _click_handler(self, event: tk.Event):
        tile_idx = self._click_pos_to_tile_idx(event.x, event.y)
        state = self.gameloop(tile_idx)
        if state == tile.YELLOW:
            self.title("Yellow won!")
        elif state == tile.RED:
            self.title("Red won!")
        self._redraw()
        if state:
            self.lock()

    def _click_pos_to_tile_idx(self, x: int, y: int) -> tuple[int, int]:
        return (
            int((y - self.padding_px) / (self.tilesize_px + self.padding_px)),
            int((x - self.padding_px) / (self.tilesize_px + self.padding_px)),
        )
    
    def gameloop(self, tile_idx: tuple[int, int]) -> tile:
        _, col = tile_idx
        row = self.highest_empty_row(col)
        if row is None:
            return
        
        self.board[row, col] = tile.RED if self.turn else tile.YELLOW
        self.turn ^= 1
        return self.check_state()
        
    
    def highest_empty_row(self, column: int) -> int | None:
        bcol = self.board[:, column] != tile.EMPTY
        if np.all(bcol):
            return None
        return int(np.argmax(bcol)) - 1
    
    def check_state(self) -> tile:
        for idxs in self._four_in_a_row_idx_iter():
            if np.all(self.board[idxs] == tile.YELLOW):
                return tile.YELLOW
            if np.all(self.board[idxs] == tile.RED):
                return tile.RED
        return False
                
    def _four_in_a_row_idx_iter(self):
        def check_idx(idx):
            y, x = idx
            return 0 <= x < self.game_width and 0 <= y < self.game_height
        for y in range(self.game_height):
            for x in range(self.game_width):
                for dy, dx in [
                    (0, 1),
                    (1, 0),
                    (1, 1),
                    (1, -1),
                ]:
                    idxs = [(y + dy * i, x + dx * i) for i in range(4)]
                    if all(map(check_idx, idxs)):
                        yield tuple(np.asarray(idxs).T.tolist())