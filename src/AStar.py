import math
from typing import *


class AStarElement:

    def __init__(self, pos: Tuple[int, int], heuristic: float, path: List[Tuple[int, int]]):
        self.pos = pos
        self.heuristic = heuristic
        self.path = path

    def __lt__(self, other: Any):
        return self.heuristic < other.heuristic


class AStar:

    def __init__(self, start: Tuple[int, int], end: Tuple[int, int], blocked_fields: List[Tuple[int, int]]):
        self.start = start
        self.end = end
        self.blocked_fields = blocked_fields

    def shortest_path(self):
        pass

    @staticmethod
    def sorted_insert(work_list: List[Any], element: Any):
        insert_i = 0
        slice_list = work_list.copy()

        while len(slice_list) > 0:
            i = len(slice_list) // 2
            if slice_list[i] < element:
                insert_i += i+1
                slice_list = slice_list[i+1:]
            else:
                slice_list = slice_list[:i]

        return work_list.insert(insert_i, element)

    @staticmethod
    def euler_dist(first_tup: Tuple[int, int], second_tup: Tuple[int, int]):
        y1, x1 = first_tup
        y2, x2 = second_tup
        return math.sqrt((y1 - y2)**2 + (x1 - x2)**2)
