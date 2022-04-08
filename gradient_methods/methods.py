import numpy as np
import function
import scipy.optimize as opt


class Solver:

    def __init__(self, func, grad_func, hessian, x0=np.array([0, 0]), alpha0=1, delta=0.5, epsilon=0.5):
        self.func = func
        self.grad_func = grad_func
        self.hessian = hessian
        self.x0 = x0
        self.alpha0 = alpha0
        self.delta = delta
        self.epsilon = epsilon
        self.xk = []

    def grad_descent(self, error):
        self.xk = []
        x = self.x0
        self.xk.append(x)

        x = self.grad_descent_iteration(x)
        k = 1

        while np.linalg.norm(self.xk[k] - self.xk[k-1], 2) > error:
            x = self.grad_descent_iteration(x)
            k += 1

        return self.xk

    def grad_descent_iteration(self, x):
        grad = self.grad_func(x)
        alpha = opt.minimize_scalar(lambda a: self.func(x - a * grad), bounds=(0, 1)).x
        x = x - alpha * grad
        self.xk.append(x)
        return x

    # alpha is initial value of step size, delta is shrink coef
    # see more at http://www.machinelearning.ru/wiki/index.php?title=%D0%9C%D0%B5%D1%82%D0%BE%D0%B4_%D0%B3%D1%80%D0%B0%D0%B4%D0%B8%D0%B5%D0%BD%D1%82%D0%BD%D0%BE%D0%B3%D0%BE_%D1%81%D0%BF%D1%83%D1%81%D0%BA%D0%B0
    # at this site our alpha is denoted as lambda
    def second_order_descent(self, error):
        self.xk = []
        x = self.x0
        self.xk.append(x)

        x = self.second_order_desc_iteration(x)
        k = 1

        while np.linalg.norm(self.xk[k] - self.xk[k - 1], 2) > error:
            x = self.second_order_desc_iteration(x)
            k += 1

        return self.xk

    def second_order_desc_iteration(self, x):
        p = np.linalg.solve(self.hessian(x), -self.grad_func(x))
        alpha = self.step_size(x, p)
        # 4th slide 7th lecture
        x = x + alpha * p
        self.xk.append(x)
        return x

    def step_size(self, x, p):
        grad_T = (self.grad_func(x)).T

        alpha = self.alpha0
        while self.func(x + alpha * p) > self.func(x) + self.epsilon * alpha * grad_T.dot(p):
            alpha *= self.delta
        return alpha

    # # notation from wikipedia page : https://en.wikipedia.org/wiki/Nonlinear_conjugate_gradient_method
    # def PR_conjugate_grad(self, eps):
    #     self.xk = []
    #     x = self.fx0
    #     self.xk.append(x)
    #
    #     grad_cur = self.grad_func(x)
    #     alpha = opt.minimize_scalar(lambda a: self.func(x - a * grad_cur), bounds=(0, 1)).x
    #     x = x - alpha * grad_cur
    #     self.xk.append(x)
    #     s = -grad_cur
    #     k = 1
    #
    #     while np.linalg.norm(self.xk[k] - self.xk[k - 1], 2) > eps:
    #         grad_prev = grad_cur
    #         grad_cur = function.grad(x)
    #         beta = grad_cur.dot(grad_cur - grad_prev) / (np.linalg.norm(grad_prev, 2)) ** 2
    #         s = -grad_cur + beta * s
    #         alpha = opt.minimize_scalar(lambda a: self.func(x + a * s), bounds=(0, 1)).x
    #         x = x + alpha * s
    #         self.xk.append(x)
    #         k = k + 1
    #
    #     return self.xk




