import numpy as np
from enum import Enum


class Method(Enum):
    UPWIND = 1
    SQUARE = 2
    LAX_WN = 3
    LAXTVD = 4


class Function(Enum):
    STEP_FUNC = 1
    PARABOLA = 2
    EXP_FUNC = 3
    SIN_FUNC = 4


# настройки

speed = 1.5
x_min = 0.0
x_max = 4.5
t_start = 0.0
t_max = (x_max - 1.5) / speed

h = 0.001
courant = 0.7
tau = courant * h / speed

frames_per_save = 1

method = Method.UPWIND.name
func = Function.PARABOLA.name

# ------


def step_func(x, x0, eps):
    xi = np.abs((x - x0) / eps)
    return np.heaviside(1.0 - xi, 0.0)


def parabola(x, x0, eps):
    xi = np.abs((x - x0) / eps)
    return (1.0 - xi ** 2) * np.heaviside(1.0 - xi, 0.0)


def exp_func(x, x0, eps):
    xi = np.abs((x - x0) / eps)
    return np.exp(-xi ** 2 / np.abs(1.0 - xi ** 2)) * np.heaviside(1.0 - xi, 0.0)


def sin_func(x, x0, eps):
    xi = np.abs((x - x0) / eps)
    return np.cos(0.5 * np.pi * xi) ** 3 * np.heaviside(1.0 - xi, 0.0)


x0 = 0.5
t0 = 0.8
eps = 0.45


if func == 'STEP_FUNC':
    phi = lambda x: step_func(x, x0=x0, eps=eps)
    mu = lambda t: step_func(t, x0=t0, eps=eps)
elif func == 'PARABOLA':
    phi = lambda x: parabola(x, x0=x0, eps=eps)
    mu = lambda t: parabola(t, x0=t0, eps=eps)
elif func == 'EXP_FUNC':
    phi = lambda x: exp_func(x, x0=x0, eps=eps)
    mu = lambda t: exp_func(t, x0=t0, eps=eps)
elif func == 'SIN_FUNC':
    phi = lambda x: sin_func(x, x0=x0, eps=eps)
    mu = lambda t: sin_func(t, x0=t0, eps=eps)


def exact(x, t):
    res = np.zeros_like(x)
    idx1 = np.nonzero(x < speed * t)
    res[idx1] = mu(t - x[idx1] / speed)
    idx2 = np.nonzero(x >= speed * t)
    res[idx2] = phi(x[idx2] - speed * t)
    return res
