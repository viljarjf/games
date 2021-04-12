from . import gui, game, solver

if __name__ == "__main__":
    m = gui.MineSweeperTkinter(10, 10, 10)
    m.run()