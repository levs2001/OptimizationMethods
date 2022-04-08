import numpy as np


def f(x: np.array) -> float:
    return x[0]**2 + np.exp(x[0]**2 + 2 * x[1]**2) + 4 * x[0] + 3 * x[1]


def grad(x: np.array) -> np.array:
    dx = 2 * x[0] + 2 * x[0] * np.exp(x[0]**2 + 2 * x[1]**2) + 4
    dy = 4 * x[1] * np.exp(x[0]**2 + 2 * x[1]**2) + 3
    return np.array([dx, dy])


def hessian(x: np.array) -> np.array:
    exp = np.exp(x[0]**2 + 2 * x[1]**2)
    h11 = 4 * x[0]**2 * exp + 2 * exp + 2
    h12 = h21 = 8 * x[0] * x[1] * exp
    h22 = 16 * x[1]**2 * exp + 4 * exp
    return np.array([[h11, h12],
                     [h21, h22]])


