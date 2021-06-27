import pygame
import pygame.freetype
import time

from .level import Level
from .config import *
from .player import Player, Point

__all__ = ["Game"]


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
        for i in range(config.WINDOW_HEIGHT_TILES):
            for j in range(config.WINDOW_WIDTH_TILES):
                if self.level.view()[j, i]:
                    arr[
                        i*self._options.tilesize:(i+1)*self._options.tilesize, 
                        j*self._options.tilesize:(j+1)*self._options.tilesize
                        ] = 0x303030
                else:
                    arr[i*self._options.tilesize:(i+1)*self._options.tilesize, 
                        j*self._options.tilesize:(j+1)*self._options.tilesize
                        ] = 0xffffff

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