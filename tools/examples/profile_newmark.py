import numpy as np
from owlfft import newmark_integrate

acc = np.loadtxt('C:\\Users\\miguelmaso\\source\\repos\\dynamics\\ipython\\AcMx1985.txt', skiprows=2)
acc /= 10

import profile
def integrate():
    for i in range(5000):
        newmark_integrate(0.02, acc, frequency=10.0, damping=0.05)
profile.run('integrate()')
