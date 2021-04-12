from . import gui, game

if __name__ == "__main__":
    m = gui.MineSweeperTkinter(30, 30, 100)
    m.run_solver()