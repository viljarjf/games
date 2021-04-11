import tkinter
import game


class MineSweeperTkinter(game.MineSweeper):

    def __init__(self, height: int, width: int, bombs: int):

        self._root = tkinter.Tk()

        super().__init__(height, width, bombs)


m = MineSweeperTkinter(10, 10, 10)
m.test()