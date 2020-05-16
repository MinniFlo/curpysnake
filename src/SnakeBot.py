from SnakeLogic import Direction


class SnakeBot:

    def __init__(self, snake):
        self.snake = snake
        # idle bot path
        self.idle_path = []
        # idle bot counter direction
        self.tup_dir = {0: (0, 2), 1: (1, 0), 2: (0, -2), 3: (-1, 0)}
        # the path the bot has found
        self.bot_path = []
        # the last path that was drawn
        self.last_bot_path = []
        # bot path char
        self.path_char = chr(8728)
        # # cycle_bot_counter
        # self.cycle_counter = 0
        # # var for mod operator
        # self.cycle_size = 4

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
        next_tup = self.dead_end_check(self.bot_path[0], (cur_y, cur_x), self.snake.tabu_fields)
        # translates the next field, to go to, into a direction
        next_direction = self.tup_to_direction(self.snake.direction, (cur_y, cur_x), next_tup)
        return next_direction

    def idle_bot(self):
        head_tup = self.snake.head.get_coordinates()
        tabu_fields = self.snake.tabu_fields.copy()
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
            best_path = []
            for path in results:
                if len(path) > len(best_path):
                    best_path = path

            if len(best_path) == 0:
                # snake just goes ahead
                return self.snake.direction

            if len(best_path) > len(self.idle_path):
                self.idle_path = best_path

        next_tup = self.idle_path.pop(0)
        next_direction = self.tup_to_direction(self.snake.direction, head_tup, next_tup)
        return next_direction

    def dead_end_check(self, next_tup, head_tup, tabu_fields):
        check_tups = self.neighbors(next_tup)
        tabu_count = 0
        for tup in check_tups:
            if tup in tabu_fields or tup == head_tup:
                tabu_count += 1
        if tabu_count >= 2:
            next_tup_count = self.flood_fill_counter(next_tup, tabu_fields)
            if next_tup_count >= (len(self.snake.snake_fields)):
                return next_tup
            choices_list = [i for i in self.neighbors(head_tup) if i not in tabu_fields and i != next_tup]
            best_choice = (next_tup, next_tup_count)
            for choice in choices_list:
                field_count = self.flood_fill_counter(choice, tabu_fields)
                if field_count > best_choice[1]:
                    best_choice = (choice, field_count)
            return best_choice[0]
        return next_tup

    @staticmethod
    def flood_fill_counter(start_tup, tabu_fields):
        field_set = {start_tup}
        work_list = [start_tup]
        while True:
            temp_list = []
            for cur_tup in work_list:
                work_list.remove(cur_tup)
                check_tups = SnakeBot.neighbors(cur_tup)
                for tup in check_tups:
                    if tup not in tabu_fields and tup not in field_set:
                        field_set.add(tup)
                        temp_list.append(tup)
            if len(temp_list) == 0:
                break
            work_list = temp_list
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

        # def cycle_bot(self):
    #     if self.cycle_counter == 0:
    #         self.cycle_counter = (self.cycle_counter + 1) % self.cycle_size
    #         return Direction.DOWN
    #     elif self.cycle_counter == 1:
    #         self.cycle_counter = (self.cycle_counter + 1) % self.cycle_size
    #         return Direction.LEFT
    #     elif self.cycle_counter == 2:
    #         self.cycle_counter = (self.cycle_counter + 1) % self.cycle_size
    #         return Direction.UP
    #     elif self.cycle_counter == 3:
    #         self.cycle_counter = (self.cycle_counter + 1) % self.cycle_size
    #         self.cycle_size += 1
    #         return Direction.RIGHT

    # does not work with current structure

    # def path_bot(self):
    #     y, x = self.snake.head.get_coordinates()
    #     if x == 56 and self.snake.direction == Direction.RIGHT:
    #         return Direction.DOWN
    #         return Direction.LEFT
    #     elif x == 4 and y != 14 and self.snake.direction == Direction.LEFT:
    #         return Direction.DOWN
    #         return Direction.RIGHT
    #     elif x == 2 and y == 14:
    #         return Direction.UP
    #     elif x == 2 and y == 1:
    #         return Direction.RIGHT
