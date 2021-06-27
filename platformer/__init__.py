from numpy.lib.histograms import histogram
import pygame
from pygame.constants import VIDEOEXPOSE
import pygame.freetype
import time
from dataclasses import dataclass, field
from typing import Tuple, List
import numpy as np

__all__ = ["Game"]

class Level:

    def __init__(self, world: int, level: int):
        self.levelmap = np.zeros((40,40), bool)
        self.levelmap[-2:] = True
        self.levelmap[-4:, -10:] = True
    
    def get_floor(self, x: int):
        return 40 - np.where(self.levelmap[:, x])[0][0]

@dataclass
class Point:
    x: float = 0
    y: float = 0

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        else:
            raise NotImplementedError(f"Addition not implemented between type Point and {type(other)}")
    
    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        else:
            raise NotImplementedError(f"Subtraction not implemented between type Point and {type(other)}")
    
    def __eq__(self, other):
        if isinstance(other, Point):
            return round(self.x) == round(other.x) and round(self.y) == round(other.y)
        else:
            raise NotImplementedError(f"Equality not implemented between type Point and {type(other)}")

    def __neq__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"({self.x}, {self.y})"


class Polygon:

    def __init__(self, points: List[Point]):
        self.points = points


class Rectangle(Polygon):

    def __init__(self, 
        bottom_left_corner: Point,
        top_right_corner: Point):
        self.points = [
            bottom_left_corner,
            Point(bottom_left_corner.x, top_right_corner.y),
            top_right_corner,
            Point(top_right_corner.x, bottom_left_corner.y)
        ]

    def get_corners(self) -> List[Point]:
        return self.points
    
    def get_center(self) -> Point:
        return Point(
            self.bl().x + (self.tr().x - self.bl().x)/2,
            self.bl().y + (self.tr().y - self.bl().y)/2
        )
    def bl(self):
        return self.points[0]
    def tl(self):
        return self.points[1]
    def tr(self):
        return self.points[2]
    def br(self):
        return self.points[3]



class Object:

    def __init__(self, bottom_left_corner: Point, height: float, width: float):

        self.hitbox: Rectangle = Rectangle(
            bottom_left_corner, 
            bottom_left_corner + Point(width, height)
        )
        self.x, self.y = self.hitbox.get_center().x, self.hitbox.get_center().y
        self.width, self.height = width, height

    
    def update_hitbox(self):
        if (center := Point(self.x, self.y)) != self.hitbox.get_center():
            diff = center - self.hitbox.get_center()
            for i in range(len(self.hitbox.points)):
                self.hitbox.points[i] += diff
            

class Player(Object):

    def __init__(self, bottom_left_corner: Point, height: float, width: float):

        self.v_max: float = 10 # pixels per second
        self.a: float = 0.7
        self.v: float = 0
        self.mu: float = 0.3
        self.direction: int = 0
        self.is_jumping = False
        self.start_jump = False
        self.v_jump = 0
        self.v_jump_init = 10
        self.g = 1
        self.y_min = bottom_left_corner.y + height/2

        super().__init__(bottom_left_corner, height, width)

    def jump(self):
        self.start_jump = not self.start_jump and not self.is_jumping
            

    def move(self):
        if self.start_jump:
            self.start_jump = False
            self.is_jumping = True
            self.v_jump += self.v_jump_init
            self.y += self.v_jump

        self.x += self.v
        self.v += (self.a*self.direction - self.mu*self.v)*(1-self.is_jumping)
        self.v = min(self.v, self.v_max)

        if self.y > self.y_min + self.height / 2:
            self.y += self.v_jump
            self.v_jump -= self.g

        if self.y <= self.y_min + self.height / 2:
            self.is_jumping = False
            self.v_jump = 0
            self.y = self.y_min + self.height / 2

        self.update_hitbox()
    
    def set_ground(self, y: float):
        self.y_min = y
    
    
    def __str__(self):
        return f"Speed: {self.v}\nPosition: {Point(self.x, self.y)}"
    
    def tl(self):
        return self.hitbox.tl()
    def br(self):
        return self.hitbox.br()


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



class Game:

    def __init__(self):
        pygame.init()
        self._set_default_options()

        self._screen = pygame.display.set_mode(self._options.size)
        self._screen.fill((255, 255, 255))

        self._running = True
        self._fps = None
        self._font = pygame.freetype.SysFont("Helvetica", 20)

        self._player = Player(Point(10, 10), 20, 20)

        self.level = Level(1, 1)

        
    def _set_default_options(self):
        self._options = Options()


    def execute_event(self, event):
        if event.type == pygame.QUIT:
            print("Quitting..")
            self._running = False
        

        elif event.type == pygame.KEYDOWN:
            for fps in range(1,10):       
                if event.unicode == str(fps):
                    self._options.set_fps(10*fps)
            if event.key == pygame.K_LEFT:
                self._player.direction -= 1
            elif event.key == pygame.K_RIGHT:
                self._player.direction += 1
            elif event.key == pygame.K_SPACE:
                self._player.jump()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self._player.direction += 1
            elif event.key == pygame.K_RIGHT:
                self._player.direction -= 1


    def gameloop(self):
        self._player.move()
        min_y = self.level.get_floor(round(self._player.x / self._options.tilesize)) * self._options.tilesize
        self._player.set_ground(min_y)
        timedelta = time.time() - self._render_start
        if timedelta < self._options.min_timedelta:
            time.sleep(self._options.min_timedelta - timedelta)
        timedelta = time.time() - self._render_start
        self._fps = 1/timedelta
        

    def coords_to_screen_coords(self, point: Point) -> Point:
        return Point(point.x, self._options.height - point.y)

    def render(self):

        arr = pygame.surfarray.array2d(self._screen)

        #render level
        for i, y in enumerate(range(0, self._options.height-1, self._options.tilesize)):
            for j, x in enumerate(range(0, self._options.width-1, self._options.tilesize)):
                if self.level.levelmap[j, i]:
                    arr[y:y+self._options.tilesize, x:x+self._options.tilesize] = 0x303030
                else:
                    arr[y:y+self._options.tilesize, x:x+self._options.tilesize] = 0xffffff

        # render player
        min = self.coords_to_screen_coords(self._player.tl())
        max = self.coords_to_screen_coords(self._player.br())
        arr[round(min.x):round(max.x), round(min.y):round(max.y)] = 0x000000


        pygame.surfarray.blit_array(self._screen, arr)

        #render fps
        self._font.render_to(self._screen, (40, 50), f"{self._fps = :.2f}", (0, 0, 0))

        pygame.display.flip()


    def first_gameloop(self):
        self._fps = 0


    def cleanup(self):
        pygame.quit()


    def start(self):
        
        # calculate the first frame
        self.first_gameloop()

        while( self._running ):
            self._render_start = time.time()

            # start by rendering the previous frame
            self.render()

            # calculate the next frame
            for event in pygame.event.get():
                self.execute_event(event)
            self.gameloop()
            
        self.cleanup()