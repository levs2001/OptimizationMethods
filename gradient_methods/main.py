import numpy as np
from  findMinimum.methods import Uniform
import function
import scipy.optimize as opt
from methods import Solver
import scipy.stats as stat
import matplotlib.pyplot as plt


def prove_orthogonality(x0, alpha0):
    eps = 1e-2
    solver = Solver(function.f, function.grad)
    xk = solver.grad_descent(x0, alpha0, eps)
    dx_last = xk[-1] - xk[-2]
    dx_before_last = xk[-2] - xk[-3]
    print(f'inner product of 2 last gradient lines: {np.inner(dx_last, dx_before_last)}') # ~ 10e-11


# run in jupyter or smth
def prove_linear_convergence(x0, alpha0):
    solver = Solver(function.f, function.grad)
    iters = []
    for err in [10**(-i) for i in range(1, 9)]:
        iters.append(solver.grad_descent(x0, alpha0, err))

    # iters = np.array([5, 6, 8, 10, 11, 13, 14, 16])
    error = np.array([i for i in range(1, 9)])  # converted from 10**(-i) to i for plotting and regression

    regr = stat.linregress(error, iters)

    plt.xlabel("iterations")
    plt.ylabel("-log10(eps)")
    plt.legend(['data', 'linear regression'])
    plt.plot(error, iters, error, regr.intercept + regr.slope * error, '--')


def solve_for_dif_error(x0, alpha0, errors, solution):
    solver = Solver(function.f, function.grad)
    for err in errors:
        x = solver.grad_descent(x0, alpha0, err)
        print(f'error: {err}; |xk - x*|_2 = {np.linalg.norm(x[-1] - solution, 2)}')


if __name__ == '__main__':

    solution = np.array([-0.65993096, -0.36934539])
    eps = 1e-2
    alpha = 0.5
    x = np.array([1.5, 2.3])

    # smh convergence is too fast, mb stop criteria is too strong
    solver = Solver(function.f, function.grad)
    xk = solver.PR_conjugate_grad(x, alpha, eps)
    for ind, xx in enumerate(xk):
        print(f'iter {ind}: error {np.linalg.norm(xx - solution, 2)}')

