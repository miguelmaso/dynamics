import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-dark-palette')

savefig = True
showfig = False

def H_simple(gamma, xi):
    return 1/np.sqrt((1-gamma**2)**2 + 2*xi*gamma)

def H_TMD(gamma, xi, eta, rho):
    a = eta**2 - gamma**2
    b = 2*xi*gamma*eta
    c = a**2 + b**2
    d = (a*(1-gamma**2) -rho*gamma**2*eta**2)**2 + b**2*(1-gamma**2*(1+rho))**2
    return np.sqrt(c/d)

rho = 0.05
gammas = np.linspace(0, 2, 500)
xi = 0.1
eta_opt = 1 / (1+rho)


# Frequency sensitivity
eta_1 = eta_opt - 0.05
eta_2 = eta_opt
eta_3 = eta_opt + 0.05
DF_0 = H_simple(gammas, xi=0)
H_eta = lambda e, g=gammas: H_TMD(g, xi=xi, eta=e, rho=rho)
Df_1 = H_eta(eta_1)
Df_2 = H_eta(eta_2)
Df_3 = H_eta(eta_3)

# Frequencies plot
fig, ax = plt.subplots()
ax.fill_between(gammas, DF_0, color='lightgray')
ax.plot(gammas, Df_1)
ax.plot(gammas, Df_2)
ax.plot(gammas, Df_3)
H_eta_1 = H_eta(eta_1,1.005)
H_eta_2 = H_eta(eta_2,1.03)
H_eta_3 = H_eta(eta_3,1.06)
ax.annotate(f'$\eta$={eta_1:.2f}', xy=(1.01, H_eta_1), xytext=(1.5, H_eta_1-.1), arrowprops=dict(arrowstyle="->"))
ax.annotate(f'$\eta$={eta_2:.2f}', xy=(1.03, H_eta_2), xytext=(1.5, H_eta_2-.1), arrowprops=dict(arrowstyle="->"))
ax.annotate(f'$\eta$={eta_3:.2f}', xy=(1.06, H_eta_3), xytext=(1.5, H_eta_3-.1), arrowprops=dict(arrowstyle="->"))
ax.text(0.1, 8.5, r'$\rho$=5%'+'\n'+r'$\xi_d$=10%', bbox=dict(facecolor='lightgray', alpha=0.5))
ax.set(xlim=(0, 2), xticks=np.arange(.5, 2, .5), xlabel='$\gamma=\Omega/\omega$',
       ylim=(0, 10), yticks=np.arange(1, 10), ylabel='$H$')
ax.grid(True)
if savefig: plt.savefig('tmd-frequencies.pdf')


# Damping sentitivity
xi_opt = np.sqrt(3*rho/8/(1+rho)**3)
xi_opt = np.sqrt(rho*(3-np.sqrt(0.5*rho))/8/(1+rho)/(1-0.5*rho))
xi_1 = xi_opt - 0.07
xi_2 = xi_opt
xi_3 = xi_opt + 0.07
H_xi = lambda x, g=gammas: H_TMD(g, xi=x, eta=eta_opt, rho=rho)
Df_1 = H_xi(xi_1)
Df_2 = H_xi(xi_2)
Df_3 = H_xi(xi_3)

# Dampings plot
fig, ax = plt.subplots()
ax.fill_between(gammas, DF_0, color='lightgray')
ax.plot(gammas, Df_1)
ax.plot(gammas, Df_2)
ax.plot(gammas, Df_3)
H_xi_1 = H_xi(xi_1, 1.0)
H_xi_2 = H_xi(xi_2, 1.0)
H_xi_3 = H_xi(xi_3, 1.0)
ax.annotate(r'$\xi_d$='+f'{xi_1*100:.0f}%', xy=(1.0, H_xi_1), xytext=(1.5, H_xi_1-.1), arrowprops=dict(arrowstyle="->"))
ax.annotate(r'$\xi_d$='+f'{xi_2*100:.0f}%', xy=(1.0, H_xi_2), xytext=(1.5, H_xi_2-.1), arrowprops=dict(arrowstyle="->"))
ax.annotate(r'$\xi_d$='+f'{xi_3*100:.0f}%', xy=(1.0, H_xi_3), xytext=(1.5, H_xi_3-.1), arrowprops=dict(arrowstyle="->"))
ax.text(0.1, 8.5, r'$\rho$=5%'+'\n'+'$\eta$='+f'{eta_opt:.2f}', bbox=dict(facecolor='lightgray', alpha=0.5))
ax.set(xlim=(0, 2), xticks=np.arange(.5, 2, .5), xlabel='$\gamma=\Omega/\omega$',
       ylim=(0, 10), yticks=np.arange(1, 10), ylabel='$H$')
ax.grid(True)
if savefig: plt.savefig('tmd-dampings.pdf')
if showfig: plt.show()
