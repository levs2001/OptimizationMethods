from findMinimum import function as fun
import methods as m

# Метод дихотомии
result_x, result_fx = m.Uniform(fun.Function.F, fun.Function.LEFT_BORDER, fun.Function.RIGHT_BORDER, fun.Function.EPSILON)

with open("resUniform.txt", 'w') as f:
    print("x :", result_x, file=f)
    print("f(x) :", result_fx, file=f)
    print("count calls :", fun.Function.counter, file=f)
    print("epsilon :", fun.Function.EPSILON, file=f)

fun.Function.counter = 0

result_x, result_fx, result_a, result_b = m.Fibonacci(fun.Function.F, fun.Function.LEFT_BORDER, fun.Function.RIGHT_BORDER, fun.Function.EPSILON)

with open("resFibonacci.txt", 'w') as f:
    print("x :", result_x, file=f)
    print("f(x) :", result_fx, file=f)
    print("Segment = [", result_a, ",", result_b, "]", file=f)
    print("count calls :", fun.Function.counter, file=f)
    print("epsilon :", fun.Function.EPSILON, file=f)