import curses


class PauseWin:

    def __init__(self, main_win):
        self.win = curses.newwin(5, 11, 4, 24)
        self.main_win = main_win
        self.index = 0
        self.fun_map = {0: self.resume, 1: self.restart, 2: self.exit}
        self.string_map = {0: "resume".ljust(7, ' '), 1: "restart", 2: "exit".ljust(7, ' ')}

    def input(self, irrer_elefant):     # be ware of the insane elephant
        cur_key = self.win.getch()
        if cur_key in [ord('w'), ord('k'), 259]:
            self.index = (self.index - 1) % 3
        elif cur_key in [ord('s'), ord('j'), 258]:
            self.index = (self.index + 1) % 3
        elif cur_key in [ord(' '), 10]:
            self.fun_map[self.index]()
        elif cur_key in [ord('q'), 27]:
            self.resume()

    def render(self):
        self.win.box()
        for i in self.string_map:
            if self.index == i:
                self.win.addstr(i + 1, 2, self.string_map[i], curses.A_REVERSE)
            else:
                self.win.addstr(i + 1, 2, self.string_map[i])

    def resume(self):
        self.main_win.change_funs(self.main_win.render, self.main_win.input, self.main_win.snake.delay)

    def restart(self):
        self.main_win.reset()
        self.resume()

    def exit(self):
        self.main_win.run = False
