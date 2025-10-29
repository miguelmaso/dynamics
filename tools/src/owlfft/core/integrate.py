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
