# from fibonacci import fibo
from functools import cache


@cache
def fibo(n):
    if (n == 0) or (n == 1):
        return 1
    else:
        return fibo(n-1)+fibo(n-2)

# Выбираем отрезки так:
# aa = c - r; bb = c + r, где
# r = k * (b - a), где k = 0.01
def Uniform(func, a, b, eps):
    print("Start point =", a)
    while a <= b:
        aa = a + eps
        if func(aa) <= func(a):
            a = aa
        else:
            break

    print("Result: x =", a, "f(x) =", func(a))

    return a, func(a)


def Fibonacci(func, a, b, eps):
    delta = 0.001

    # n = 5
    # fib = fibo(n)
    # N = (b - a) / eps
    # while N > fib:
    #     n += 1
    #     fib = fibo(n)

    # print(f'Fn={fibo(n)}')
    # print(f'n={n}')
    s = 20


    while b - a > eps:
        k = 1
        l = (b - a) / fibo(s)
        lymda = a + l * fibo(s - 2)
        mu = a + l * fibo(s - 1)
        a, b = FibonacciCycle(func, a, b, s, k, lymda, mu, delta)
        print("Segment outer = [", a, b, f"], {b-a}")


    res = (a + b) / 2
    print("Result: x =", res, "f(x) =", func(res), "Segment = [", a, b, "]")
    return res, func(res), a, b


def FibonacciCycle(func, a, b, s, k, lymda, mu, delta):
    print("Segment = [", a, b, f"], {b - a}")
    if func(lymda) > func(mu):
        a = lymda
        lymda = mu
        mu = a + (b - a) * fibo(s - 1 - k) / fibo(s - k)
        if k == s - 2:
            if func(lymda) > func(lymda + delta):
                return lymda, b
            else:
                return a, lymda + delta
        else:
            return FibonacciCycle(func, a, b, s, k + 1, lymda, mu, delta)
    else:
        b = mu
        mu = lymda
        lymda = a + (b - a) * fibo(s - 2 - k) / fibo(s - k)
        if k == s - 2:
            if func(lymda) > func(lymda + delta):
                return lymda, b
            else:
                return a, lymda + delta
        else:
            return FibonacciCycle(func, a, b, s, k + 1, lymda, mu, delta)
