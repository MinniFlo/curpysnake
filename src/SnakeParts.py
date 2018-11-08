

class Head:

    def __init__(self, y, x, color):
        self.y, self.x = (y, x)
        self.symbol = chr(9654)
        # self.symbol = 'o'
        self.color = color

    def get_coordinates(self):
        return self.y, self.x

    def set_coordinates(self, y, x):
        self.y = y
        self.x = x

    def set_color(self, color):
        self.color = color


class BodyPart:

    def __init__(self, y, x, color):
        self.y, self.x = (y, x)
        self.symbol = chr(9642)
        # self.symbol = '#'
        self.color = color

    def get_coordinates(self):
        return self.y, self.x

    def set_coordinates(self, y, x):
        self.y = y
        self.x = x

    def set_color(self, color):
        self.color = color


class Food:

    def __init__(self, y, x, ):
        self.y, self.x = (y, x)
        self.symbol = chr(9672)
        # self.symbol = 'X'

    def get_coordinates(self):
        return self.y, self.x

    def set_coordinates(self, y, x):
        self.y = y
        self.x = x
