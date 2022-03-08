import numpy as np

from simplex_method.simplex_method import step, starting_vector

ZERO = 1e-10

if __name__ == '__main__':

    # primal canon
    A = [
        [1, 4, 0, 1, 7, -7, 0, 0],
        [7, 6, 0, 0, 4, -4, 0, 0],
        [4, 0, 2, 1, 6, -6, 0, 0],
        [5, 1, 6, 0, 8, -8, 1, 0],
        [1, 0, 0, 2, 7, -7, 0, -1]
    ]
    b = [5, 2, 1, 9, 4]
    c = [2, 4, 5, 0, 0, 0, 0, 0]

    # dual canon
    # A = [
    #     [-5, 1, 1, 0, 0, 0, 1, -1, 7, -7, 4, -4],
    #     [-1, 0, 0, 1, 0, 0, 4, -4, 6, -6, 0, 0],
    #     [-6, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, -2],
    #     [0, 2, 0, 0, 0, 1, 1, -1, 0, 0, 1, -1],
    #     [-8, 7, 0, 0, 0, 0, 7, -7, 4, -4, 6, -6]
    # ]
    # b = [2, 4, 5, 0, 0]
    # c = [9, -4, 0, 0, 0, 0, -5, 5, -2, 2, -1, 1]

    A = np.array(A)
    b = np.array(b)
    c = np.array(c)
    xk = starting_vector(A, b, c)
    max_iterations = 20
    Nk = None
    solution_found = False
    for i in range(max_iterations):
        if np.any(xk < 0):
            raise ValueError("negative xk[j] found")

        xk, Nk, solution_found = step(A, b, c, xk)
        print(f'iter {i}: xk = {xk}')
        if solution_found:
            print(f'solution: {xk}')
            print(f'number of iterations: {i + 1}')
            print(f'target function: {np.round(c.dot(xk), decimals=10)}')
            break

    if not solution_found:
        print(f"solution hasn't been found in {max_iterations} iterations")

    # res = opt.linprog(cc, A_eq=AA, b_eq=bb, method='simplex')
    # print(res)


























    # todo свести дуальную задачу к каноническому виду - в неканоническом решается правильно
    # [primal] non canon
    # A_eq = [
    #     [1, 4, 0, 1, 7],
    #     [7, 6, 0, 0, 4],
    #     [4, 0, 2, 1, 6]
    # ]
    # b_eq = [5, 2, 1]
    # A_le = [
    #     [5, 1, 6, 0, 8],
    #     [-1, 0, 0, -2, -7]
    # ]
    # b_le = [9, -4]
    # c = [2, 4, 5, 0, 0]
    # bounds = [
    #     [0, None],
    #     [0, None],
    #     [0, None],
    #     [0, None],
    #     [None, None]
    # ]
    # print(3 * '-----\n')
    # res = opt.linprog(c, A_ub=A_le, b_ub=b_le, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='simplex')
    # print(res)


