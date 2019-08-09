from SnakeLogic import *
from Pause import PauseWin
import time


class Window:

    def __init__(self, win, snake):
        self.win = win
        self.snake = snake
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
        # the path the bot has found
        self.bot_path = []
        # the last path that was drawn
        self.last_bot_path = []
        # bot path char
        self.path_char = chr(8728)
        # idle bot path
        self.idle_path = []
        # idle bot counter direction
        self.tup_dir = {0: (0, 2), 1: (1, 0), 2: (0, -2), 3: (-1, 0)}

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
        self.flood_bot()

        if cur_key in [ord('q'), 27]:
            self.change_funs(self.pause_win.render, self.pause_win.input, 0.01)
        time.sleep(0.01)

    # bots -------------------------------------------------------------------------------------------------------------

    def path_bot(self):
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

    def flood_bot(self):
        # A* algorithm
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
                to_check_tups = {(y - 1, x), (y + 1, x), (y, x - 2), (y, x + 2)}
                for tup in to_check_tups:
                    # sorts out all not reachable fields
                    if step == 1:
                        if tup not in self.snake.tabu_fields:
                            step_dict[step].add(tup)
                    else:
                        if tup not in self.snake.tabu_fields and tup not in step_dict[step - 2]:
                            step_dict[step].add(tup)
            # if no path to the target was found bot needs to idle
            if step >= 150:
                self.idle_bot()
                return
            # if the target is in the reachable fields the loop stops
            if (food_y, food_x) in step_dict[step]:
                target_reached = True
            # else there will be another step
            else:
                step += 1
        self.idle_path.clear()
        self.bot_path.clear()
        # saves the path to the target
        self.bot_path = [(food_y, food_x)]
        # the first steps that will be worked on are the previous of the target step
        step -= 1
        # build the path from the target to the start backwards
        while step > 0:
            work_y, work_x = self.bot_path[0]
            to_find_tups = [(work_y - 1, work_x), (work_y + 1, work_x), (work_y, work_x - 2), (work_y, work_x + 2)]
            for tup in to_find_tups:
                if tup in step_dict[step]:
                    self.bot_path.insert(0, tup)
                    break
            step -= 1
        # translates the next field to got to into a direction
        next_tup = self.bot_path[0]
        next_direction = self.tup_to_direction(self.snake.direction, (cur_y, cur_x), next_tup)
        self.update_buffer(next_direction)

    def idle_bot(self):
        head_tup = self.snake.head.get_coordinates()
        tabu_fields = self.snake.tabu_fields
        if len(self.idle_path) == 0:
            # saves the 4 idle paths
            results = []

            for i in range(4):
                # safes the current path
                cur_list = []
                # index for the offset dict
                tup_dict_index = (i - 1) % 4
                # alternates between -1, 0, 1 and determines the cur_dir_index
                offset_pointer = -1
                # shows in witch direction the offset_pointer evolves
                offset_dir_flag = True
                work_tup = head_tup
                if tuple(map(self.add_tup, work_tup, self.tup_dir[tup_dict_index])) in tabu_fields:
                    tup_dict_index = (tup_dict_index + 2) % 4
                    offset_pointer = 1
                    offset_dir_flag = False

                fields_left = True
                while fields_left:
                    if offset_pointer != 0:
                        next_field = tuple(map(self.add_tup, work_tup, self.tup_dir[tup_dict_index]))
                        if next_field in tabu_fields or \
                                tuple(map(self.add_tup, next_field, self.tup_dir[i])) in tabu_fields:
                            tup_dict_index = i
                            if offset_pointer == -1:
                                offset_dir_flag = True
                            else:
                                offset_dir_flag = False
                            offset_pointer = 0
                        else:
                            cur_list.append(next_field)
                            work_tup = next_field
                    else:
                        next_field = tuple(map(self.add_tup, work_tup, self.tup_dir[tup_dict_index]))
                        if next_field in tabu_fields:
                            fields_left = False
                        else:
                            if offset_dir_flag:
                                offset_pointer += 1
                                # distance_buffer = (2, 2)
                            else:
                                offset_pointer -= 1
                                # distance_buffer = (1, 1)
                            tup_dict_index = (tup_dict_index + offset_pointer) % 4
                            cur_list.append(next_field)
                            work_tup = next_field

                results.append(cur_list)

            # calculate the longest idle path
            best_path = []
            for path in results:
                if len(path) > len(best_path):
                    best_path = path

            if len(best_path) == 0:
                # todo: emergency_idle
                self.update_buffer(self.snake.direction)
                return
            else:
                self.idle_path = best_path

        next_tup = self.idle_path.pop(0)
        next_direction = self.tup_to_direction(self.snake.direction, head_tup, next_tup)
        self.update_buffer(next_direction)

    @staticmethod
    def add_tup(tup_val1, tup_val2):
        return tup_val1 + tup_val2

    @staticmethod
    def mul_tup(tup_val, fac_val):
        return tup_val * fac_val

    @staticmethod
    def tup_to_direction(cur_direction, start, target):
        (cur_y, cur_x) = start
        (next_y, next_x) = target
        if next_y == cur_y:
            if next_x > cur_x:
                if cur_direction != Direction.RIGHT:
                    return Direction.RIGHT
            else:
                if cur_direction != Direction.LEFT:
                    return Direction.LEFT
        else:
            if next_y > cur_y:
                if cur_direction != Direction.DOWN:
                    return Direction.DOWN
            else:
                if cur_direction != Direction.UP:
                    return Direction.UP

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
            current = time.time()
            if current - timestamp >= self.delay:
                # the bot only needs to input once before the render
                self.input_fun(self.buffer_direction[0])
                self.render_fun()
                timestamp = current
