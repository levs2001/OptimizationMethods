import numpy as np
import gradient_methods.function as fun


class Problem:

    def __init__(self):
        pass

    @staticmethod
    def bound_func(x: np.array) -> np.array:
        return np.array([
            -2 * x[0] - 5 * x[1] - 5,
            -x[0] + 3 * x[1] - 1,
            x[0] ** 2 - 1.5,
            fun.f(np.array([x[0], x[1]])) - x[2]
        ])

    @staticmethod
    def bound_grad(x: np.array) -> np.array:
        return np.array([
            np.array([-2, -5, 0]),
            np.array([-1, 3, 0]),
            np.array([2 * x[0], 0, 0]),
            np.append(fun.grad(np.array([x[0], x[1]])), -1)
        ])

    @staticmethod
    def bound_subgrad(x: np.array) -> np.array:
        phi = Problem.bound_func(x)
        maximum = max(phi)
        maximum_index = [i for i, val in enumerate(phi) if val == maximum][0]
        return Problem.bound_grad(x)[maximum_index]


