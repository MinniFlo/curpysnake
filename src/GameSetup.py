from GameWindow import Window
from SnakeLogic import *


class Setup:

    def __init__(self, scr, args):
        self.scr = scr
        self.args = args
        self.max_y, self.max_x = 16, 59
        self.win = curses.newwin(self.max_y, self.max_x, 0, 0)
        self.logic = Snake(self.max_y, self.max_x)
        self.game = Window(self.win, self.logic)


    def args_stuff(self):
        if self.args.walls:
            self.logic.move = self.logic.walls_movement

    def create_game(self):
        self.args_stuff()
        return self.game
