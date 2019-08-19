from SnakeParts import *
from enum import Enum
import curses
import random


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Snake:
    def __init__(self, max_y, max_x, color, color_num):
        self.max_y, self.max_x = max_y, max_x
        self.color = color
        self.head = Head(1, 8, curses.color_pair(self.color.color_num))
        self.body = []
        self.food = Food(1, 1)
        self.direction = Direction.RIGHT
        self.tabu_fields = set()
        self.rim_fields = set()
        self.all_fields = set()
        self.snake_fields = set()
        self.loose = False
        self.win = False
        self.score = 0
        self.score_msg = " Score: 00{} ".format(self.score)
        self.delay = 0.5
        self.move = self.free_movement
        self.color_fun = self.color.calc_color
        self.color_fun_map = {1: self.color.blue_red_color, 2: self.color.red_green_color,
                              3: self.color.green_blue_color, 4: self.color.random_color}
        if color_num is not None:
            self.color_fun = self.color_fun_map[color_num]
        self.ugly = False

    def reset_snake(self):
        self.head.set_coordinates(1, 8)
        self.body.clear()
        self.snake_fields.clear()
        self.loose = False
        self.score = 0
        self.score_msg = " Score: 00{} ".format(self.score)
        self.direction = Direction.RIGHT
        self.head.symbol = chr(9654)
        self.delay = 0.01

    def init_sake(self):
        self.reset_snake()
        cur_y, cur_x = self.head.get_coordinates()
        for _ in range(3):
            cur_x -= 2
            color = curses.color_pair(self.color.color_num)
            body = BodyPart(cur_y, cur_x, color)
            self.body.append(body)
        self.fill_all_fields()
        self.fill_rim_fields()
        self.update_tabu_fields()
        self.update_food_pos()

    def update_snake_pos(self):
        pre_y, pre_x = self.head.get_coordinates()
        pre_head_color = self.head.color
        self.move(pre_y, pre_x)
        color = self.color_fun()
        self.head.set_color(color)
        if self.ugly:
            self.delay = ((random.randrange(20, 75)) / 100) ** 3

        if self.food.get_coordinates() == self.head.get_coordinates():
            new_body = BodyPart(pre_y, pre_x, pre_head_color)
            self.body.insert(0, new_body)
            self.update_tabu_fields()
            self.update_food_pos()
            self.update_score()
        else:
            moved_body = self.body.pop()
            moved_body.set_coordinates(pre_y, pre_x)
            moved_body.set_color(pre_head_color)
            self.body.insert(0, moved_body)
            self.update_tabu_fields()

    def update_food_pos(self):
        work_fields = self.all_fields - self.tabu_fields
        work_fields = list(work_fields)
        if work_fields:
            cur_y, cur_x = random.choice(work_fields)
            self.food.set_coordinates(cur_y, cur_x)
            if self.delay > 0.1:
                if self.score % 5 == 0:
                    self.delay -= 0.01
        else:
            self.win = True

    # todo: more efficient pls
    def update_tabu_fields(self):
        self.tabu_fields.clear()
        self.snake_fields.clear()
        head_y, head_x = self.head.get_coordinates()
        self.snake_fields.add((head_y, head_x))
        for i in self.body:
            body_y, body_x = i.get_coordinates()
            self.snake_fields.add((body_y, body_x))
        self.tabu_fields = self.snake_fields | self.rim_fields

    def fill_rim_fields(self):
        top_y, top_x = 0, 0
        bot_y, bot_x = self.max_y - 1, self.max_x - 1
        for i in range(self.max_x):
            self.rim_fields.add((top_y, i))
            self.rim_fields.add((bot_y, i))
        for i in range(self.max_y):
            self.rim_fields.add((i, top_x))
            self.rim_fields.add((i, bot_x))

    def fill_all_fields(self):
        for i in range(self.max_y):
            for j in range(self.max_x):
                if j % 2 != 0:
                    continue
                self.all_fields.add((i, j))

    def update_score(self):
        self.score += 1
        self.score_msg = " Score: {} ".format(str(self.score).rjust(3, "0"))

    def walls_movement(self, pre_y, pre_x):
        if self.direction == Direction.UP:
            self.head.set_coordinates(pre_y - 1, pre_x)
        elif self.direction == Direction.DOWN:
            self.head.set_coordinates(pre_y + 1, pre_x)
        elif self.direction == Direction.LEFT:
            self.head.set_coordinates(pre_y, pre_x - 2)
        elif self.direction == Direction.RIGHT:
            self.head.set_coordinates(pre_y, pre_x + 2)
        if self.head.get_coordinates() in self.tabu_fields:
            self.loose = True

    def free_movement(self, pre_y, pre_x):
        if self.direction == Direction.UP:
            if pre_y - 1 != 0:
                self.head.set_coordinates(pre_y - 1, pre_x)
            else:
                self.head.set_coordinates(self.max_y - 2, pre_x)
        elif self.direction == Direction.DOWN:
            if pre_y + 1 != self.max_y - 1:
                self.head.set_coordinates(pre_y + 1, pre_x)
            else:
                self.head.set_coordinates(1, pre_x)
        elif self.direction == Direction.LEFT:
            if pre_x - 2 != 0:
                self.head.set_coordinates(pre_y, pre_x - 2)
            else:
                self.head.set_coordinates(pre_y, self.max_x - 3)
        elif self.direction == Direction.RIGHT:
            if pre_x + 2 != self.max_x - 1:
                self.head.set_coordinates(pre_y, pre_x + 2)
            else:
                self.head.set_coordinates(pre_y, 2)
        for i in self.body:
            if i.get_coordinates() == self.head.get_coordinates():
                self.loose = True
