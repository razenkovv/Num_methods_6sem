import numpy as np
from enum import Enum

# wave equation
# u_tt = c*u_xx + f(x,t), where c1,c2 = const
# x [lft,rgt]
# t > 0
# u(x,0) = f_0(x)
# u_t(x,0) = f_0t(x)
# a1*u(lft,t) + a2*u_x(lft,t) = f_lft(t)
# b1*u(rgt,t) + b2*u_x(rgt,t) = f_rgt(t)

lft = 0.0
rgt = 1.0

c = 0.5

a1 = 0.0
a2 = 1.0

b1 = 1.0
b2 = -1.0


def f(x, t):
    return 0.5 * (2 + 2 * np.cos(t - x) + x * np.sin(t - x)) / (1 + np.cos(t - x)) ** 2


def f_0(x):
    return x - x * np.tan(x / 2)


def f_0xx(x):
    return -0.5 * (x * np.tan(x/2) + 2) / (np.cos(x/2))**2


def f_0t(x):
    return 1 + x / (1 + np.cos(x))


def f_lft(t):
    return 1 + np.tan(t / 2)


def f_rgt(t):
    return t + 1 / (1 + np.cos(t - 1))


def exact(x, t):
    return t + x + x * np.tan(0.5 * (t - x))


class Method(Enum):
    CROSS_1 = 1
    CROSS_2 = 2


method = 'CROSS_2'

h = 0.01
courant = 0.5

t_start = 0.0
t_end = 1.0

frames_per_save = 1
path = f'data/{method}_h={h}_c={courant}_frpersave={frames_per_save}.csv'

n = int((rgt - lft) / h) + 1
tau = courant * h / np.sqrt(c)
mesh = np.linspace(lft, rgt, n)
timesteps = np.arange(t_start, t_end, tau)


def error_estimation(e):
    return np.max(np.abs(e))
    #return np.mean(np.abs(e))
    #return np.sqrt(sum(e**2)/len(e))
