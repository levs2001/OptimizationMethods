import numpy as np
from  findMinimum.methods import Uniform
import function
import scipy.optimize as opt
from methods import Solver
import scipy.stats as stat
import matplotlib.pyplot as plt


def prove_orthogonality(solver):
    eps = 1e-2
    xk = solver.grad_descent(eps)
    dx_last = xk[-1] - xk[-2]
    dx_before_last = xk[-2] - xk[-3]
    print(f'inner product of 2 last gradient lines: {np.inner(dx_last, dx_before_last)}') # ~ 1e-11


# run in jupyter or smth
def prove_linear_convergence(solver):
    iters = []
    for err in [10**(-i) for i in range(1, 9)]:
        iters.append(solver.grad_descent(err))

    error = np.array([i for i in range(1, 9)])  # converted from 10**(-i) to i for plotting and regression
    regr = stat.linregress(error, iters)

    plt.xlabel("iterations")
    plt.ylabel("-log10(eps)")
    plt.legend(['data', 'linear regression'])
    plt.plot(error, iters, error, regr.intercept + regr.slope * error, '--')


def solve_for_dif_error(solver_method, errors, solution):
    for err in errors:
        x = solver_method(err)
        print(f'given error: {err}; |xk - x*|_2 = {np.linalg.norm(x[-1] - solution, 2)}')


if __name__ == '__main__':

    solution = np.array([-0.65993096, -0.36934539])
    eps = 1e-2
    alpha = 0.5
    x = np.array([1.5, 2.3])
    solver = Solver(function.f, function.grad, function.hessian)

    errors = [0.1, 0.01, 0.001]
    solve_for_dif_error(solver.grad_descent, errors, solution)

    solve_for_dif_error(solver.second_order_descent, errors, solution)




