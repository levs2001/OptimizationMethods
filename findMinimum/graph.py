from matplotlib import pyplot as plt
import numpy as np
from findMinimum import function as f

y = np.vectorize(f.Function.F)
x = np.linspace(f.Function.LEFT_BORDER, f.Function.RIGHT_BORDER, 100)

plt.plot(x, y(x))
plt.xlabel("x")
plt.ylabel("F(x)")
plt.grid()
plt.show()
