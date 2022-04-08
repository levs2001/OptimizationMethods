import numpy as np
import function
import scipy.optimize as opt


class Solver:

    def __init__(self, func, grad_func):
        self.func = func
        self.grad_func = grad_func
        self.xk = []

    def grad_descent(self, x0, alpha0, eps):
        self.xk = []
        x = x0
        self.xk.append(x)

        grad = self.grad_func(x)
        alpha = opt.minimize_scalar(lambda a: self.func(x - a * grad), bounds=(0, 1)).x
        x = x - alpha * grad
        self.xk.append(x)
        k = 1

        while np.linalg.norm(self.xk[k] - self.xk[k-1], 2) > eps:
            grad = function.grad(x)
            alpha = opt.minimize_scalar(lambda a: self.func(x - a * grad), bounds=(0, 1)).x
            # alpha, _ = Uniform(lambda a: function.f(x - a * grad), 0, 1, alpha_eps)
            x = x - alpha * grad
            self.xk.append(x)
            k = k + 1

        return self.xk


    # notation from wikipedia page : https://en.wikipedia.org/wiki/Nonlinear_conjugate_gradient_method
    def PR_conjugate_grad(self, x0, alpha0, eps):
        self.xk = []
        x = x0
        self.xk.append(x)

        grad_cur = self.grad_func(x)
        alpha = opt.minimize_scalar(lambda a: self.func(x - a * grad_cur), bounds=(0, 1)).x
        x = x - alpha * grad_cur
        self.xk.append(x)
        s = -grad_cur
        k = 1

        while np.linalg.norm(self.xk[k] - self.xk[k - 1], 2) > eps:
            grad_prev = grad_cur
            grad_cur = function.grad(x)
            beta = grad_cur.dot(grad_cur - grad_prev) / (np.linalg.norm(grad_prev, 2)) ** 2
            s = -grad_cur + beta * s
            alpha = opt.minimize_scalar(lambda a: self.func(x + a * s), bounds=(0, 1)).x
            x = x + alpha * s
            self.xk.append(x)
            k = k + 1

        return self.xk




