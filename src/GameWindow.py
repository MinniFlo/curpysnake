from SnakeLogic import *
from SnakeBot import SnakeBot
from Pause import PauseWin
import time


class Window:

    def __init__(self, win, snake):
        self.win = win
        self.snake = snake
        self.snake_bot = SnakeBot(snake)
        self.pause_win = PauseWin(self)
        self.debug_win = curses.newwin(16, 40, 0, 60)
        self.input_fun = self.input
        self.render_fun = self.render
        self.delay = self.snake.delay
        self.freeze = True
        self.run = True
        self.direction_symbol_map = {Direction.RIGHT: chr(9654), Direction.LEFT: chr(9664),
                                     Direction.UP: chr(9650), Direction.DOWN: chr(9660)}
        # self.direction_symbol_map = {Direction.RIGHT: 'O', Direction.LEFT: 'O',
        #                              Direction.UP: 'O', Direction.DOWN: 'O'}
        self.buffer_direction = {0: None, 1: None}

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
        # draw bot path
        for y, x in self.snake_bot.bot_path:
            self.win.addstr(y, x, self.snake_bot.path_char, curses.color_pair(25))
        self.snake_bot.last_bot_path = self.snake_bot.bot_path.copy()
        # draw food
        food_y, food_x = self.snake.food.get_coordinates()
        self.win.addstr(food_y, food_x, self.snake.food.symbol)
        # draw snake body
        for body in self.snake.body:
            body_y, body_x = body.get_coordinates()
            self.win.addstr(body_y, body_x, body.symbol, body.color)
        # draw snake head
        head_y, head_x = self.snake.head.get_coordinates()
        self.win.addstr(head_y, head_x, self.snake.head.symbol, self.snake.head.color)

    def clear_snake(self):
        # clear last path
        for y, x in self.snake_bot.last_bot_path:
            self.win.addstr(y, x, ' ')
        # clear body
        for body in self.snake.body:
            y, x = body.get_coordinates()
            self.win.addstr(y, x, ' ')
        # clear head
        pre_y, pre_x = self.snake.head.get_coordinates()
        self.win.addstr(pre_y, pre_x, ' ')

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

        # bot_movement input
        if not self.freeze:
            self.update_buffer(self.snake_bot.cycle_bot())

        if cur_key in [ord('q'), 27]:
            self.change_funs(self.pause_win.render, self.pause_win.input, 0.01)
        time.sleep(0.01)

    def update_buffer(self, direction):
        if direction is None:
            self.buffer_direction[0] = self.buffer_direction[1]
            self.buffer_direction[1] = None
        elif self.buffer_direction[0] is None:
            self.buffer_direction[0] = direction
        elif self.buffer_direction[1] is None:
            self.buffer_direction[1] = direction

    def render(self):
        if not self.freeze:

            # evaluate direction buffer if a new direction is on the stack
            if self.buffer_direction[0] is not None:
                # update snake direction
                self.snake.direction = self.buffer_direction[0]
                # update snake head char
                self.snake.head.symbol = self.direction_symbol_map[self.buffer_direction[0]]
                # delete the processed direction from the buffer
                self.update_buffer(None)

            self.clear_snake()

            self.snake.update_snake_pos()

            self.draw_snake()

            self.win.addstr(0, 2, self.snake.score_msg)

            if self.snake.loose or self.snake.win:
                self.freeze = True
                self.delay = 0.01
            self.delay = self.snake.delay

    def reset(self):
        self.snake.init_sake()
        self.buffer_direction = {0: Direction.RIGHT, 1: None}
        self.freeze = True
        self.draw()

    def game_loop(self):
        self.setup()

        timestamp = time.time()
        while self.run:
            current = time.time()
            if current - timestamp >= self.delay:
                # the bot only needs to input once before the render
                self.input_fun(self.buffer_direction[0])
                self.render_fun()
                timestamp = current
