import numpy as np
from pygame import constants
from . import config

class Level:

    def __init__(self, world: int, level: int):
        self.levelmap = np.zeros((40,40), bool)
        self.levelmap[-2:] = True
        self.levelmap[-4:, -10:] = True
        self.x_offset: int = 0
        self.y_offset: int = 0
    
    def get_floor(self, x: int):
        return config.WINDOW_HEIGHT_TILES - np.where(self.levelmap[:, x])[0][0]
    
    def view(self):
        return self.levelmap[
            self.y_offset:self.y_offset + config.WINDOW_HEIGHT_TILES,
            self.x_offset:self.x_offset + config.WINDOW_WIDTH_TILES
        ]