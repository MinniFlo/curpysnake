from SnakeLogic import Direction
import math
import logging


class SnakeBot:

    def __init__(self, snake):
        self.snake = snake
        # idle bot path
        self.idle_path = []
        # counts idle steps till recalculation of idle_path
        self.idle_count = 0
        # idle bot counter direction
        self.tup_dir = {0: (0, 2), 1: (1, 0), 2: (0, -2), 3: (-1, 0)}
        # the path the bot has found
        self.bot_path = []
        # the last path that was drawn
        self.last_bot_path = []
        # bot path char
        self.path_char = chr(8728)

        # debug logging
        logging.basicConfig(filename="debug.log", level=logging.INFO)

    def flood_bot(self):
        # A* algorithm
        # start coordinates
        cur_y, cur_x = self.snake.head.get_coordinates()
        # target coordinates
        food_y, food_x = self.snake.food.get_coordinates()
        future_tabu_fields = self.snake.tabu_fields.copy()
        # is used to track the snake body
        future_snake = self.snake.body.copy()
        future_snake.pop()
        # saves all reachable fields. the key is the distance
        step_dict = {0: {(cur_y, cur_x)}}
        # flag for the while loop
        target_reached = False
        # counts the steps
        step = 1
        while not target_reached:
            # inits new set for the new steps
            step_dict[step] = set()

            # removes the snake part from the tabu fields that disappeared in this step
            if len(future_snake) > 0 and step > 1:
                remove_tup = future_snake.pop().get_coordinates()
                future_tabu_fields.remove(remove_tup)

            # iter over the last reached fields
            for tup in step_dict[step - 1]:
                # all neighbor fields
                to_check_tups = self.neighbors(tup)
                for neighbor in to_check_tups:
                    # sorts out all not reachable fields
                    if step == 1:
                        if neighbor not in future_tabu_fields:
                            step_dict[step].add(neighbor)
                    else:
                        if neighbor not in future_tabu_fields and neighbor not in step_dict[step - 2]:
                            step_dict[step].add(neighbor)
            # if no path to the target was found bot needs to idle
            if step >= 150:
                return self.idle_bot()
            # if the target is in the reachable fields the loop stops
            if (food_y, food_x) in step_dict[step]:
                target_reached = True
            # else there will be another step
            else:
                step += 1

        self.idle_path.clear()
        self.idle_count = 0
        self.bot_path.clear()
        # saves the path to the target
        self.bot_path = [(food_y, food_x)]
        # the first steps that will be worked on are the previous of the target step
        step -= 1
        # build the path from the target to the start backwards
        while step > 0:
            work_tup = self.bot_path[0]
            to_find_tups = self.neighbors(work_tup)
            candidate = ()
            for tup in to_find_tups:
                if tup in step_dict[step]:
                    candidate = tup
                    break
            self.bot_path.insert(0, candidate)
            step -= 1
        # checks if the snake will run into a dead end and returns the next tup
        next_tup = self.dead_end_check(self.bot_path[0], (cur_y, cur_x), self.snake.tabu_fields.copy())
        # translates the next field, to go to, into a direction
        next_direction = self.tup_to_direction(self.snake.direction, (cur_y, cur_x), next_tup)
        return next_direction

    def idle_bot(self):
        head_tup = self.snake.head.get_coordinates()
        if self.idle_count < 5 and len(self.idle_path) > 0:
            self.idle_count = 1
            next_tup = self.idle_path.pop(0)
            next_direction = self.tup_to_direction(self.snake.direction, head_tup, next_tup)
            return next_direction

        tabu_fields = self.snake.tabu_fields.copy()
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
            # is the field the algorithem is currently at
            work_tup = head_tup
            # counts the steps to prevent that the bot loops across the whole game win
            step_counter = 0
            if tuple(map(self.add_tup, work_tup, self.tup_dir[tup_dict_index])) in tabu_fields:
                tup_dict_index = (tup_dict_index + 2) % 4
                offset_pointer = 1
                offset_dir_flag = False

            fields_left = True
            while fields_left:
                if offset_pointer != 0:
                    step_counter += 1
                    next_field = tuple(map(self.add_tup, work_tup, self.tup_dir[tup_dict_index]))
                    if next_field in tabu_fields or \
                            tuple(map(self.add_tup, next_field, self.tup_dir[i])) in tabu_fields or \
                            ((i == 0 or i == 2) and step_counter >= 13) or \
                            ((i == 1 or i == 3) and step_counter >= 27):
                        step_counter = 0
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

        for path in results:
            if len(path) > len(self.idle_path):
                self.idle_path = path

        if len(self.idle_path) == 0:
            # snake just goes ahead
            return self.snake.direction

        next_tup = self.idle_path.pop(0)
        next_direction = self.tup_to_direction(self.snake.direction, head_tup, next_tup)
        self.idle_count += 1
        return next_direction

    def dead_end_check(self, next_tup, head_tup, tabu_fields):
        # body_last = self.snake.body[-1].get_coordinates()
        # if body_last in self.far_neighbors(head_tup):
        #     return next_tup
        tabu_fields.add(head_tup)
        snake_end = self.snake.body[-1]
        head_neighbors = self.neighbors(head_tup)
        next_tup_count = self.flood_fill_counter(next_tup, tabu_fields, snake_end)
        if next_tup_count >= (len(self.snake.snake_fields)):
            return next_tup
        best_choice = (next_tup, next_tup_count)
        choices_list = [i for i in head_tup if i not in tabu_fields and i != next_tup]
        for choice in choices_list:
            field_count = self.flood_fill_counter(choice, tabu_fields, snake_end)
            if field_count > best_choice[1]:
                best_choice = (choice, field_count)
        return best_choice[0]

    @staticmethod
    def flood_fill_counter(start_tup, tabu_fields, snake_end):
        field_set = set()
        work_list = [start_tup]
        while len(work_list) > 0:
            # temp_list = []
            cur_tup = work_list.pop()
            if cur_tup in tabu_fields or cur_tup in field_set:
                if cur_tup == snake_end:
                    return math.inf
                continue
            else:
                work_list.extend(SnakeBot.neighbors(cur_tup))
                field_set.add(cur_tup)
        return len(field_set)

    @staticmethod
    def add_tup(tup_val1, tup_val2):
        return tup_val1 + tup_val2

    @staticmethod
    def mul_tup(tup_val, fac_val):
        return tup_val * fac_val

    @staticmethod
    def neighbors(tup):
        y, x = tup
        return [(y - 1, x), (y + 1, x), (y, x - 2), (y, x + 2)]

    @staticmethod
    def far_neighbors(tup):
        y, x = tup
        return {(y - 1, x), (y + 1, x), (y, x - 2), (y, x + 2), (y - 1, x - 2), (y + 1, x + 2),
                (y - 1, x + 2), (y + 1, x - 2), (y - 2, x), (y + 2, x), (y, x - 4), (y, x + 4)}

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
