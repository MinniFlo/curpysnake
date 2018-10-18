import curses
import random


class Color:

    def __init__(self, color_num):
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
        curses.init_color(13, color_0, color_0, color_255)      # blue
        curses.init_color(14, color_128, color_0, color_255)
        curses.init_color(15, color_191, color_0, color_255)
        curses.init_color(16, color_224, color_0, color_255)
        curses.init_color(17, color_255, color_0, color_255)
        curses.init_color(18, color_255, color_0, color_224)
        curses.init_color(19, color_255, color_0, color_191)
        curses.init_color(20, color_255, color_0, color_128)
        curses.init_color(21, color_255, color_0, color_0)      # red
        curses.init_color(22, color_255, color_128, color_0)
        curses.init_color(23, color_255, color_191, color_0)
        curses.init_color(24, color_255, color_224, color_0)
        curses.init_color(25, color_255, color_255, color_0)
        curses.init_color(26, color_224, color_255, color_0)
        curses.init_color(27, color_191, color_255, color_0)
        curses.init_color(28, color_128, color_255, color_0)
        curses.init_color(29, color_0, color_255, color_0)      # green
        curses.init_color(30, color_0, color_255, color_128)
        curses.init_color(31, color_0, color_255, color_191)
        curses.init_color(32, color_0, color_255, color_224)

        # curses.init_pair(1, 9, -1)
        # curses.init_pair(2, 10, -1)
        # curses.init_pair(3, 11, -1)
        # curses.init_pair(4, 12, -1)
        # curses.init_pair(5, 13, -1)   # blue
        # curses.init_pair(6, 14, -1)
        # curses.init_pair(7, 15, -1)
        # curses.init_pair(8, 16, -1)
        # curses.init_pair(9, 17, -1)
        # curses.init_pair(10, 18, -1)
        # curses.init_pair(11, 19, -1)
        # curses.init_pair(12, 20, -1)
        # curses.init_pair(13, 21, -1)  # red
        # curses.init_pair(14, 22, -1)
        # curses.init_pair(15, 23, -1)
        # curses.init_pair(16, 24, -1)
        # curses.init_pair(17, 25, -1)
        # curses.init_pair(18, 26, -1)
        # curses.init_pair(19, 27, -1)
        # curses.init_pair(20, 28, -1)
        # curses.init_pair(21, 29, -1)  # green
        # curses.init_pair(22, 30, -1)
        # curses.init_pair(23, 31, -1)
        # curses.init_pair(24, 32, -1)

        for i in range(1, 25):
            curses.init_pair(i, i+8, -1)

        self.color_num = color_num
        self.display_num = 0
        self.color_cycle = 0
        self.blue_red_map = {0: 5, 1: 6, 2: 7, 3: 8, 4: 9, 5: 10, 6: 11, 7: 12, 8: 13}
        self.red_green_map = {0: 13, 1: 14, 2: 15, 3: 16, 4: 17, 5: 18, 6: 19, 7: 20, 8: 21}
        self.green_blue_map = {0: 21, 1: 22, 2: 23, 3: 24, 4: 1, 5: 2, 6: 3, 7: 4, 8: 5}
        self.map_reverse = False

    def blue_red_color(self):
        if self.color_cycle == 0:
            if not self.map_reverse:
                self.color_num += 1
                if self.color_num == 8:
                    self.map_reverse = True
            else:
                self.color_num -= 1
                if self.color_num == 0:
                    self.map_reverse = False
        self.color_cycle = (self.color_cycle + 1) % 3
        return curses.color_pair(self.blue_red_map[self.color_num])

    def red_green_color(self):
        if self.color_cycle == 0:
            if not self.map_reverse:
                self.color_num += 1
                if self.color_num == 8:
                    self.map_reverse = True
            else:
                self.color_num -= 1
                if self.color_num == 0:
                    self.map_reverse = False
        self.color_cycle = (self.color_cycle + 1) % 3
        return curses.color_pair(self.red_green_map[self.color_num])

    def green_blue_color(self):
        if self.color_cycle == 0:
            if not self.map_reverse:
                self.color_num += 1
                if self.color_num == 8:
                    self.map_reverse = True
            else:
                self.color_num -= 1
                if self.color_num == 0:
                    self.map_reverse = False
        self.color_cycle = (self.color_cycle + 1) % 3
        return curses.color_pair(self.green_blue_map[self.color_num])

    def calc_color(self):
        if self.color_cycle == 0:
            self.color_num = (self.color_num % 24) + 1
        self.color_cycle = (self.color_cycle + 1) % 3
        return curses.color_pair(self.color_num)

    def random_color(self):
        return curses.color_pair(random.randrange(1, 25))
