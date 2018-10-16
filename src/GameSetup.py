from GameWindow import Window
from SnakeLogic import *


class Setup:

    def __init__(self, scr):
        self.scr = scr
        self.max_y, self.max_x = 16, 59
        self.win = curses.newwin(self.max_y, self.max_x, 0, 0)
        self.logic = Snake(self.max_y, self.max_x)
        self.game = Window(scr, self.logic)
