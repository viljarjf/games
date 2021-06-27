from dataclasses import dataclass, field
from typing import Tuple

@dataclass
class Options:
    max_fps: int = 60
    min_timedelta: float = field(init=False)

    height: int = 800
    width: int = 800
    size: Tuple[int, int] = height, width

    tilesize = 20

    def __post_init__(self):
        self.min_timedelta = 1/self.max_fps
    
    def set_fps(self, fps: int):
        self.max_fps = fps
        self.min_timedelta = 1/self.max_fps
    
WINDOW_HEIGHT_PIXELS = 800
WINDOW_WIDTH_PIXELS = 800
TILESIZE = 20
WINDOW_WIDTH_TILES = WINDOW_WIDTH_PIXELS // TILESIZE
WINDOW_HEIGHT_TILES = WINDOW_HEIGHT_PIXELS // TILESIZE
