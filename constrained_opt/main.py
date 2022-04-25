import numpy as np

from constrained_opt.problem import Problem
from simplex import simplex_solve


def find_s0():
    x1_bounds = [-1.5 ** 0.5, 1.5 ** 0.5]
    x2_low = min((-5 - 2 * x1_bounds[0]) / 5, (-5 - 2 * x1_bounds[1]) / 5,
                 (x1_bounds[0] + 1) / 3, (x1_bounds[1] + 1) / 3)
    x2_high = max((-5 - 2 * x1_bounds[0]) / 5, (-5 - 2 * x1_bounds[1]) / 5,
                  (x1_bounds[0] + 1) / 3, (x1_bounds[1] + 1) / 3)

    x2_bounds = [x2_low, x2_high]
    x3_bounds = [-6.401, 30]
    return [x1_bounds, x2_bounds, x3_bounds]


if __name__ == '__main__':
    solution = np.array([-0.65993096, -0.36934539])
    k = 0
    eps = 0.001
    s0 = find_s0()
    A = np.array([
        [1, 0, 0],
        [-1, 0, 0],
        [0, 1, 0],
        [0, -1, 0],
        [0, 0, 1],
        [0, 0, -1]
    ])
    b = np.array([s0[0][1], -s0[0][0], s0[1][1], -s0[1][0], s0[2][1], -s0[2][0]])
    c = np.array([0, 0, 1])
    yk, xk = simplex_solve(A.T, -c, b)


    ak = np.array([Problem.bound_subgrad(xk)])
    bk = - np.max(Problem.bound_func(xk)) + ak.dot(xk)
    A = np.append(A, ak, axis=0)
    b = np.append(b, bk)
    yk, xk_next = simplex_solve(A.T, -c, b, np.append(yk, 0))

    while np.linalg.norm(xk_next - xk, 2) > eps:
        print(f'err: {np.linalg.norm(xk_next - xk, 2)}')
        xk = xk_next
        ak = np.array([Problem.bound_subgrad(xk)])
        bk = - np.max(Problem.bound_func(xk)) + ak.dot(xk)
        A = np.append(A, ak, axis=0)
        b = np.append(b, bk)
        yk, xk_next = simplex_solve(A.T, -c, b, np.append(yk, 0))
        k += 1

    print(f'iter: {k}, err: {np.linalg.norm(xk_next - xk, 2)}')
    print(f'{xk_next}')

    xk_next = np.array([xk_next[0], xk_next[1]])
    print(f'actual error: {np.linalg.norm(xk_next - solution, 2)}')

    # res = opt.linprog(c, A_ub=A, b_ub=b, method='simplex')
    # print(res)
    # cons = ({'type': 'ineq', 'fun': lambda x: 2 * x[0] + 5 * x[1] + 5},
    #         {'type': 'ineq', 'fun': lambda x: x[0] - 3 * x[1] + 1},
    #         {'type': 'ineq', 'fun': lambda x: -x[0]**2 + 1.5})
    #
    # print(opt.minimize(fun.f, np.array([0, 0]), constraints=cons))

