from . import gui, game

if __name__ == "__main__":
    m = gui.MineSweeperTkinter(20, 20, 79)
    m.run_solver()