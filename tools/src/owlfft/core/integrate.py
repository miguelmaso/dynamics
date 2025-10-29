import numpy as np


def newmark_integrate(t, f, mass=None, friction=None, stiffness=None, frequency=None, damping=None, u0=0.0, v0=0.0, beta=1/4, gamma=1/2):
    '''
    Integrate a single degree of freedom system using the Newmark method.

    Parameters
    ----------
    t : float|array_like
        Time step or time vector (can be non-uniform).
    f : array_like
        External force time series (same length as t, if t is array_like).
    mass, friction, stiffness : float, optional
        Mass, friction coefficient, stiffness.
    frequency, damping: float, optional
        Frequency and damping. Frequency and stiffness are mutually exclusive. Damping and friction are mutually exclusive.
        If mass is not specified, the time series will be considered an acceleration.
    u0, v0 : float, optional
        Initial displacement and velocity.
    beta, gamma : float, optional
        Newmark integration parameters. 
        (Default corresponds to average acceleration method (beta=1/4, gamma=1/2): unconditional stability).

    Returns
    -------
    u, v, a : ndarray
        Arrays of displacement, velocity, and acceleration.
    '''
    if frequency is not None:
        if stiffness:
            raise Exception('Frequency and stiffness are mutually exclusive.')
        m = mass or 1.0
        k = m * frequency**2
    else:
        if mass is None or stiffness is None:
            raise Exception('Mass and stiffness are required arguments.')
        m = mass
        k = stiffness
    if damping and friction:
        raise Exception('Damping and friction are mutually exclusive.')
    damping = damping or 0.0
    c = friction or 2 * damping * np.sqrt(m*k)

    if isinstance(t, (float, int)):
        t = np.linspace(0.0, t*len(f), len(f))
    else:
        t = np.asarray(t)
        if len(t) != len(f):
            raise Exception('The length of time series and force series must match.')

    n = len(f)
    u = np.empty(n, float)
    v = np.empty(n, float)
    a = np.empty(n, float)

    Dt = np.diff(t, prepend=0)
    u[0] = un = u0
    v[0] = vn = v0
    a[0] = an = (f[0] - c*v0 - k*u0) / m

    for i in range(1,n):
        dt = Dt[i]
        v_trial = vn + dt*(1-gamma)*an
        u_trial = un + dt*vn + 0.5*dt**2*(1-2*beta)*an
        a[i] = an = (f[i] - c*v_trial - k*u_trial) / (m + gamma*c*dt + beta*k*dt**2)
        v[i] = vn = v_trial + gamma*dt*an
        u[i] = un = u_trial + beta*dt**2*an

    return u, v, a


# acc = np.loadtxt('C:\\Users\\miguelmaso\\source\\repos\\dynamics\\ipython\\AcMx1985.txt', skiprows=2)
# acc /= 10


# import profile
# def integrate():
#     for i in range(5000):
#         newmark_integrate(0.02, acc, frequency=10.0, damping=0.05)
# profile.run('integrate()')


# import matplotlib.pyplot as plt

# u, v, a = newmark_integrate(0.02, acc, frequency=10.0, damping=0.05)
# f, (ax1, ax2) = plt.subplots(2)
# t = np.linspace(0, 0.02*len(acc), len(acc))
# ax1.plot(t,acc)
# ax2.plot(t,a)
# plt.show()

# nT = 100
# Su = np.empty(nT, float)
# Sv = np.empty(nT, float)
# Sa = np.empty(nT, float)
# periods = np.linspace(0.1, 4, nT)
# for i in range(nT):
#     T = periods[i]
#     w = 2*np.pi/T
#     u, v, a = newmark_integrate(0.02, acc, frequency=w, damping=0.05)
#     Su[i] = max(u)
#     Sv[i] = max(v)
#     Sa[i] = max(a) / 9.81
# plt.plot(periods, Sa)
# plt.show()
