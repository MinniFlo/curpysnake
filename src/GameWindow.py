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
        self.direction_symbol_map = {Direction.RIGHT: chr(9654), Direction.LEFT: chr(9664),
                                     Direction.UP: chr(9650), Direction.DOWN: chr(9660)}
        # self.direction_symbol_map = {Direction.RIGHT: 'O', Direction.LEFT: 'O',
        #                              Direction.UP: 'O', Direction.DOWN: 'O'}
        self.buffer_direction = {0: None, 1: None}
        # the path the bot has found
        self.bot_path = []
        # the last path that was drawn
        self.last_bot_path = []
        # bot path char
        self.path_char = chr(8728)

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
        for y, x in self.bot_path:
            self.win.addstr(y, x, self.path_char, curses.color_pair(25))
        self.last_bot_path = self.bot_path.copy()
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
        for y, x in self.last_bot_path:
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
        self.flood_bot_input()

        if cur_key in [ord('q'), 27]:
            self.change_funs(self.pause_win.render, self.pause_win.input, 0.01)
        time.sleep(0.01)

    # bots -------------------------------------------------------------------------------------------------------------

    def path_bot_input(self):
        y, x = self.snake.head.get_coordinates()
        if x == 56 and self.snake.direction == Direction.RIGHT:
            self.update_buffer(Direction.DOWN)
            self.update_buffer(Direction.LEFT)
        elif x == 4 and y != 14 and self.snake.direction == Direction.LEFT:
            self.update_buffer(Direction.DOWN)
            self.update_buffer(Direction.RIGHT)
        elif x == 2 and y == 14:
            self.update_buffer(Direction.UP)
        elif x == 2 and y == 1:
            self.update_buffer(Direction.RIGHT)

    def flood_bot_input(self):
        # start coordinates
        cur_y, cur_x = self.snake.head.get_coordinates()
        # target coordinates
        food_y, food_x = self.snake.food.get_coordinates()
        # saves all reachable fields. the key is the distance
        step_dict = {0: {(cur_y, cur_x)}}
        # flag for the while loop
        target_reached = False
        # counts the steps
        step = 1
        while not target_reached:
            # inits new set for the new steps
            step_dict[step] = set()
            # iter over the last reached fields
            for (y, x) in step_dict[step - 1]:
                # all neighbor fields
                to_check_tups = {(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)}
                for tup in to_check_tups:
                    # sorts out all not reachable fields
                    if tup not in self.snake.tabu_fields:
                        step_dict[step].add(tup)
            # if the target is in the reachable fields the loop stops
            if (food_y, food_x) in step_dict[step]:
                target_reached = True
            # else there will be another step
            else:
                step += 1
        # saves the path to the target
        final_path = [(food_y, food_x)]
        # the first steps that will be worked on are the previous to the target step
        step -= 1
        while step > 0:
            work_y, work_x = final_path[0]
            to_find_tups = [(work_y - 1, work_x), (work_y + 1, work_x), (work_y, work_x - 1), (work_y, work_x + 1)]
            for tup in to_find_tups:
                if tup in step_dict[step]:
                    final_path.insert(0, tup)
                    break
            step -= 1
        (fin_y, fin_x) = final_path[0]
        if fin_y == cur_y:
            if fin_x > cur_x:
                self.update_buffer(Direction.RIGHT)
            else:
                self.update_buffer(Direction.LEFT)
        else:
            if fin_y > cur_y:
                self.update_buffer(Direction.DOWN)
            else:
                self.update_buffer(Direction.UP)

    # ------------------------------------------------------------------------------------------------------------------

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
            self.input_fun(self.buffer_direction[0])
            current = time.time()
            if current - timestamp >= self.delay:
                self.render_fun()
                timestamp = current

