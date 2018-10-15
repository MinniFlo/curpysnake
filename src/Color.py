import curses
import random


class Color:

    def __init__(self):
        color_255 = 1000
        color_0 = 0
        color_224 = 878
        color_191 = 749
        color_128 = 502
        curses.use_default_colors()

        curses.init_color(9, color_0, color_255, color_255)
        curses.init_color(10, color_0, color_224, color_255)
        curses.init_color(11, color_0, color_191, color_255)
        curses.init_color(12, color_0, color_128, color_255)
        curses.init_color(13, color_0, color_0, color_255)
        curses.init_color(14, color_128, color_0, color_255)
        curses.init_color(15, color_191, color_0, color_255)
        curses.init_color(16, color_224, color_0, color_255)
        curses.init_color(17, color_255, color_0, color_255)
        curses.init_color(18, color_255, color_0, color_224)
        curses.init_color(19, color_255, color_0, color_191)
        curses.init_color(20, color_255, color_0, color_128)
        curses.init_color(21, color_255, color_0, color_0)
        curses.init_color(22, color_255, color_128, color_0)
        curses.init_color(23, color_255, color_191, color_0)
        curses.init_color(24, color_255, color_224, color_0)
        curses.init_color(25, color_255, color_255, color_0)
        curses.init_color(26, color_224, color_255, color_0)
        curses.init_color(27, color_191, color_255, color_0)
        curses.init_color(28, color_128, color_255, color_0)
        curses.init_color(29, color_0, color_255, color_0)
        curses.init_color(30, color_0, color_255, color_128)
        curses.init_color(31, color_0, color_255, color_191)
        curses.init_color(32, color_0, color_255, color_224)

        curses.init_pair(1, 9, -1)
        curses.init_pair(2, 10, -1)
        curses.init_pair(3, 11, -1)
        curses.init_pair(4, 12, -1)
        curses.init_pair(5, 13, -1)
        curses.init_pair(6, 14, -1)
        curses.init_pair(7, 15, -1)
        curses.init_pair(8, 16, -1)
        curses.init_pair(9, 17, -1)
        curses.init_pair(10, 18, -1)
        curses.init_pair(11, 19, -1)
        curses.init_pair(12, 20, -1)
        curses.init_pair(13, 21, -1)
        curses.init_pair(14, 22, -1)
        curses.init_pair(15, 23, -1)
        curses.init_pair(16, 24, -1)
        curses.init_pair(17, 25, -1)
        curses.init_pair(18, 26, -1)
        curses.init_pair(19, 27, -1)
        curses.init_pair(20, 28, -1)
        curses.init_pair(21, 29, -1)
        curses.init_pair(22, 30, -1)
        curses.init_pair(23, 31, -1)
        curses.init_pair(24, 32, -1)

        self.color_num = 20
        self.color_cycle = 0

    def calc_color(self):
        if self.color_cycle == 0:
            self.color_num = (self.color_num % 24) + 1
        self.color_cycle = (self.color_cycle + 1) % 3
        return curses.color_pair(self.color_num)

    def random_color(self):
        return curses.color_pair(random.randrange(1, 25))
