from GameWindow import Window
from SnakeLogic import *
from Color import Color


class Setup:

    def __init__(self, scr, args):
        self.scr = scr
        self.args = args
        self.max_y, self.max_x = 16, 59
        self.win = curses.newwin(self.max_y, self.max_x, 0, 0)
        self.color = Color(20)
        self.logic = Snake(self.max_y, self.max_x, self.color, 0)
        self.game = Window(self.win, self.logic)

    def args_stuff(self):
        if self.args.walls:
            self.logic.move = self.logic.walls_movement
        if self.args.uglycolor:
            self.refresh_game(4)
        if self.args.randomspeed:
            self.logic.ugly = True
        if self.args.color is not None:
            self.color = Color(0)
            self.refresh_game(self.args.color)

    def create_game(self):
        self.args_stuff()
        return self.game

    def refresh_game(self, color_num):
        self.logic = Snake(self.max_y, self.max_x, self.color, color_num)
        self.game = Window(self.win, self.logic)
