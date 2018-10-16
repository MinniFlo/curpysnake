from SnakeLogic import *
from Pause import PauseWin
import time


class Window:

    def __init__(self, win, snake):
        self.win = win
        self.snake = snake
        self.pause_win = PauseWin(self)
        self.input_fun = self.input
        self.render_fun = self.render
        self.delay = self.snake.delay
        self.freeze = True
        self.run = True
        self.dir_changed = False
        self.last_key = -1
        self.direction_symbol_map = {Direction.RIGHT: chr(9654), Direction.LEFT: chr(9664),
                                     Direction.UP: chr(9650), Direction.DOWN: chr(9660)}
        self.buffer_direction = {0: Direction.RIGHT, 1: None}

    def setup(self):
        curses.noecho()
        curses.curs_set(0)
        self.win.keypad(True)
        self.pause_win.win.keypad(True)
        self.win.nodelay(True)
        self.snake.init_sake()
        self.draw()

    def draw(self):
        self.win.clear()
        self.win.box()
        self.draw_snake()
        self.win.addstr(0, 2, self.snake.score_msg)

    def draw_snake(self):
        for body in self.snake.body:
            body_y, body_x = body.get_coordinates()
            self.win.addstr(body_y, body_x, body.symbol, body.color)

        head_y, head_x = self.snake.head.get_coordinates()
        self.win.addstr(head_y, head_x, self.snake.head.symbol, self.snake.head.color)

        food_y, food_x = self.snake.food.get_coordinates()
        self.win.addstr(food_y, food_x, self.snake.food.symbol)

    def change_funs(self, render_fun, input_fun, delay):
        self.render_fun = render_fun
        self.input_fun = input_fun
        self.delay = delay

    def input(self, direction):
        if direction is None:
            direction = self.snake.direction
        cur_key = self.win.getch()
        if cur_key != -1 and self.freeze and not self.snake.loose:
            self.freeze = False
        if cur_key in [ord('w'), ord('k'), 259] and direction != Direction.UP and direction != Direction.DOWN:
            self.update_buffer(Direction.UP)
        elif cur_key in [ord('s'), ord('j'), 258] and direction != Direction.UP and direction != Direction.DOWN:
            self.update_buffer(Direction.DOWN)
        elif cur_key in [ord('a'), ord('h'), 260] and direction != Direction.LEFT and direction != Direction.RIGHT:
            self.update_buffer(Direction.LEFT)
        elif cur_key in [ord('d'), ord('l'), 261] and direction != Direction.LEFT and direction != Direction.RIGHT:
            self.update_buffer(Direction.RIGHT)
        elif cur_key in [ord('q'), 27]:
            self.change_funs(self.pause_win.render, self.pause_win.input, 0.01)
        time.sleep(0.001)

    def update_buffer(self, direction):
        if direction is None:
            self.buffer_direction[0] = self.buffer_direction[1]
            self.buffer_direction[1] = None
        elif self.buffer_direction[0] is None:
            self.buffer_direction[0] = direction
        elif self.buffer_direction[1] is None:
            self.buffer_direction[1] = direction
        else:
            pass

    def render(self):
        if not self.freeze:
            self.win.clear()
            self.win.box()

            if self.buffer_direction[0] is not None:
                self.snake.direction = self.buffer_direction[0]
                self.snake.head.symbol = self.direction_symbol_map[self.buffer_direction[0]]
                self.update_buffer(None)
            self.snake.update_snake_pos()

            self.draw_snake()

            self.win.addstr(0, 2, self.snake.score_msg)

            if self.snake.loose:
                self.freeze = True

    def reset(self):
        self.snake.init_sake()
        self.buffer_direction = {0: Direction.RIGHT, 1: None}
        self.freeze = True
        self.draw()


    def game_loop(self):
        self.setup()

        timestamp = time.time()
        while self.run:
            self.input_fun(self.buffer_direction[0])
            current = time.time()
            if current - timestamp >= self.delay:
                self.render_fun()
                timestamp = current

