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
        # y and x size of the game field
        self.max_y, self.max_x = max_y, max_x
        # instance of the color class
        self.color = color
        # snake head obj
        self.head = Head(1, 8, curses.color_pair(self.color.color_num))
        # snake body objects are saved in a list
        self.body = []
        # food obj
        self.food = Food(1, 1)
        # the direction the snake heads to
        self.direction = Direction.RIGHT
        # the fields the snake can't move on
        self.tabu_fields = set()
        # saves all fields (y, x) that are the rim of the game window
        self.rim_fields = set()
        # saves all fields (y, x) of the game Window
        self.all_fields = set()
        # saves all fields the snake is on
        self.snake_fields = set()
        self.loose = False
        self.win = False
        # number of food the snake collected
        self.score = 0
        # score string
        self.score_msg = " Score: 00{} ".format(self.score)
        # the delay between the steps the snake takes
        self.delay = 0.5
        # saves the type of movement functions the snake can do (with/without walls)
        self.move = self.free_movement
        # saves the type of color select function
        self.color_fun = self.color.calc_color
        self.color_fun_map = {1: self.color.blue_red_color, 2: self.color.red_green_color,
                              3: self.color.green_blue_color, 4: self.color.random_color}
        if color_num is not None:
            self.color_fun = self.color_fun_map[color_num]
        # activates ugly mode
        self.ugly = False

    # resets all game relevant variables
    def reset_snake(self):
        self.head.set_coordinates(1, 8)
        self.body.clear()
        self.snake_fields.clear()
        self.loose = False
        self.score = 0
        self.score_msg = " Score: 00{} ".format(self.score)
        self.direction = Direction.RIGHT
        self.head.symbol = chr(9654)
        self.delay = 0.001

    # initializes the game
    def init_sake(self):
        self.reset_snake()
        # builds snake
        cur_y, cur_x = self.head.get_coordinates()
        for _ in range(3):
            cur_x -= 2
            color = curses.color_pair(self.color.color_num)
            body = BodyPart(cur_y, cur_x, color)
            self.body.append(body)
        # ------------
        self.fill_all_fields()
        self.fill_rim_fields()
        self.init_tabu_fields()
        self.update_food_pos()

    # main function of the logic class
    def update_snake_pos(self):
        # safes last head position and color
        pre_y, pre_x = self.head.get_coordinates()
        pre_head_color = self.head.color
        # calls move function (updates head position)
        self.move(pre_y, pre_x)
        # gets the new color and sets it to the head
        color = self.color_fun()
        self.head.set_color(color)

        head_tup = self.head.get_coordinates()

        # if food was eaten
        if self.food.get_coordinates() == head_tup:
            # creates new body part and sets coordinates to the old head position and color
            new_body = BodyPart(pre_y, pre_x, pre_head_color)
            # inserts the new body part on the first position of the body
            self.body.insert(0, new_body)
            self.update_tabu_fields((pre_y, pre_x))
            self.update_food_pos()
            self.update_score()
        # the snake just moved normal
        else:
            # the last body part gets removed and saved
            moved_body = self.body.pop()
            # sets the coordinates and color of the removed body part to the coordinates and color of the old head
            moved_body.set_coordinates(pre_y, pre_x)
            moved_body.set_color(pre_head_color)
            # inserts the removed body part on the first position of the body
            self.body.insert(0, moved_body)
            self.update_tabu_fields(moved_body.get_coordinates(), self.body[len(self.body) - 1].get_coordinates())

    # sets delay time random if ugly
        if self.ugly:
            self.delay = ((random.randrange(20, 75)) / 100) ** 3

    # updates the possition of the food
    def update_food_pos(self):
        # gets all free fields
        work_fields = self.all_fields - self.tabu_fields
        work_fields.remove(self.head.get_coordinates())
        work_fields = list(work_fields)

        # if there are still free fields a new food will be set
        if work_fields:
            cur_y, cur_x = random.choice(work_fields)
            self.food.set_coordinates(cur_y, cur_x)
            # lowers the delay every five food
            if self.delay > 0.1:
                if self.score % 5 == 0:
                    self.delay -= 0.01
        # if there are no fields left win is set to true
        else:
            self.win = True

    # init the tabu fields
    def init_tabu_fields(self):
        self.tabu_fields.clear()
        self.snake_fields.clear()
        for i in range(len(self.body) - 1):
            body_tup = self.body[i].get_coordinates()
            self.snake_fields.add(body_tup)
        self.tabu_fields = self.snake_fields | self.rim_fields

    # ...
    def update_tabu_fields(self, add_tup, remove_tup = None):
        self.tabu_fields.add(add_tup)
        self.snake_fields.add(add_tup)
        if remove_tup is not None:
            self.tabu_fields.remove(remove_tup)
            self.snake_fields.remove(remove_tup)

    # fills the rim fields set
    def fill_rim_fields(self):
        top_y, top_x = 0, 0
        bot_y, bot_x = self.max_y - 1, self.max_x - 1
        for i in range(self.max_x):
            self.rim_fields.add((top_y, i))
            self.rim_fields.add((bot_y, i))
        for i in range(self.max_y):
            self.rim_fields.add((i, top_x))
            self.rim_fields.add((i, bot_x))

    # fills the all fields set
    def fill_all_fields(self):
        for i in range(self.max_y):
            for j in range(self.max_x):
                if j % 2 != 0:
                    continue
                self.all_fields.add((i, j))

    # updates score
    def update_score(self):
        self.score += 1
        self.score_msg = " Score: {} ".format(str(self.score).rjust(3, "0"))

    # sets snake head depending on the direction to the next field and ends the game. takes walls into account
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

    # sets snake head depending on the direction to the next field and ends the game. takes walls not into account
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
        if self.head.get_coordinates() in self.tabu_fields:
            self.loose = True
