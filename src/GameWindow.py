from SnakeLogic import *
import time


class Window:

    def __init__(self, scr):
        self.scr = scr
        self.max_y, self.max_x = 16, 59
        self.win = curses.newwin(self.max_y, self.max_x, 0, 0)
        self.snake = Snake(self.max_y, self.max_x)
        self.start = False
        self.run = True
        self.dir_changed = False
        self.last_key = -1
        self.direction_symbol_map = {Direction.RIGHT: chr(9654), Direction.LEFT: chr(9664),
                                     Direction.UP: chr(9650), Direction.DOWN: chr(9660)}
        self.buffer_direction = {0: Direction.RIGHT, 1: None}

    def setup(self):
        curses.noecho()
        curses.curs_set(0)
        self.win.nodelay(True)
        self.win.box()
        self.snake.init_sake()
        self.render()

    def input(self, direction):
        if direction is None:
            direction = self.snake.direction
        cur_key = self.win.getch()
        if cur_key == ord('w') and direction != Direction.UP and direction != Direction.DOWN:
            self.update_buffer(Direction.UP)
        elif cur_key == ord('s') and direction != Direction.UP and direction != Direction.DOWN:
            self.update_buffer(Direction.DOWN)
        elif cur_key == ord('a') and direction != Direction.LEFT and direction != Direction.RIGHT:
            self.update_buffer(Direction.LEFT)
        elif cur_key == ord('d') and direction != Direction.LEFT and direction != Direction.RIGHT:
            self.update_buffer(Direction.RIGHT)
        elif cur_key == 27:
            self.run = False
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
        self.win.clear()
        self.win.box()
        if self.buffer_direction[0] is not None:
            self.snake.direction = self.buffer_direction[0]
            self.snake.head.symbol = self.direction_symbol_map[self.buffer_direction[0]]
            self.update_buffer(None)
        self.snake.update_snake_pos()
        head_y, head_x = self.snake.head.get_coordinates()
        self.win.addstr(head_y, head_x, self.snake.head.symbol, self.snake.head.color)

        for body in self.snake.body:
            body_y, body_x = body.get_coordinates()
            self.win.addstr(body_y, body_x, body.symbol, body.color)

        food_y, food_x = self.snake.food.get_coordinates()
        self.win.addstr(food_y, food_x, self.snake.food.symbol)
        self.win.addstr(0, 2, self.snake.score_msg)
        if self.snake.loose:
            self.run = False

    # def render_single(self):
    #     self.snake.direction = self.buffer_direction
    #     self.snake.head.symbol = self.buffer_symbol
    #     self.snake.update_snake_pos()
    #     for i in self.snake.render_list:
    #         cur_y, cur_x = i.get_coordinates()
    #         self.win.addch(cur_y, cur_x, ' ')
    #         self.win.addch(cur_y, cur_x, i.symbol)
    #     self.win.addstr(0, 2, "Score: {}".format(self.snake.score))
    #     if self.snake.loose:
    #         self.run = False

    def game_loop(self):
        self.setup()
        timestamp = time.time()
        while self.run:
            self.input(self.buffer_direction[0])
            current = time.time()
            if current - timestamp >= self.snake.delay:
                self.render()
                timestamp = current
        self.win.getch()

