import os
import numpy as np
from matplotlib import pyplot as plt
from owlfft import newmark_integrate

dir = os.path.dirname(os.path.realpath(__file__))
acc = np.loadtxt(os.path.join(dir, 'AcMx1985.txt'), skiprows=2)
acc /= 10

nT = 100
Su = np.empty(nT, float)
Sv = np.empty(nT, float)
Sa = np.empty(nT, float)
periods = np.linspace(0.1, 4, nT)
for i in range(nT):
    T = periods[i]
    w = 2*np.pi/T
    u, v, a = newmark_integrate(0.02, acc, frequency=w, damping=0.05)
    Su[i] = max(u)
    Sv[i] = max(v)
    Sa[i] = max(a) / 9.81
plt.plot(periods, Sa)
plt.show()
