import numpy as np
from enum import Enum

# heat equation
# u_t = c*u_xx + f(x,t), where c = const
# x [lft,rgt]
# t > 0
# u(x,0) = f_0(x)
# a1*u(lft,t) + a2*u_x(lft,t) = f_lft(t)
# b1*u(rgt,t) + b2*u_x(rgt,t) = f_rgt(t)

lft = 0.0
rgt = 1.0

c = 1.0

a1 = 1.0
a2 = -1.0

b1 = 1.0
b2 = 1.0


def f(x, t):
    return -np.sinh(x-t) - np.cosh(x-t)


def f_0(x):
    return np.cosh(x)


def f_lft(t):
    return np.exp(t)


def f_rgt(t):
    return np.exp(1-t)


def exact(x, t):
    return np.cosh(x-t)


class Method(Enum):
    WEIGHT_1 = 1
    WEIGHT_2 = 2


method = 'WEIGHT_2'

h = 0.01
courant = 100
sigma = 0.5

if sigma < 0.5:
    courant = 0.25 / (1 - 2 * sigma)  # courant must be <= 1 / 2*(1-2*sigma)
    print('courant modified')


t_start = 0.0
t_end = 1.0

frames_per_save = 10
path = f'data/{method}_h={h}_c={courant}_frpersave={frames_per_save}.csv'

n = int((rgt - lft) / h) + 1
tau = courant * h**2 / c  # courant = c * tau / h**2
mesh = np.linspace(lft, rgt, n)
timesteps = np.arange(t_start, t_end, tau)


def error_estimation(e):
    return np.max(np.abs(e))
    # return np.mean(np.abs(e))
    # return np.sqrt(sum(e**2)/len(e))
