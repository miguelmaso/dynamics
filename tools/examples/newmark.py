import numpy as np
from matplotlib import pyplot as plt
from owlfft import newmark_integrate

acc = np.loadtxt('C:\\Users\\miguelmaso\\source\\repos\\dynamics\\ipython\\AcMx1985.txt', skiprows=2)
acc /= 10

u, v, a = newmark_integrate(0.02, acc, frequency=10.0, damping=0.05)
f, (ax1, ax2) = plt.subplots(2)
t = np.linspace(0, 0.02*len(acc), len(acc))
ax1.plot(t,acc)
ax2.plot(t,a)
plt.show()
