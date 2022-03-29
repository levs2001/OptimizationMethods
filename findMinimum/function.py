from functools import cache
from math import sin


class Function:
    counter = 0
    LEFT_BORDER = 0.5
    RIGHT_BORDER = 1
    EPSILON = 0.01

    @staticmethod
    @cache
    def F(x):
        Function.counter += 1
        return x * x * x - 3 * sin(x)
