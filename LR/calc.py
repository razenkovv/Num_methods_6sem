import numpy as np

import header

# u_t + a * u_x = 0
# u(x, 0) = phi(x)
# u(0, t) = mu(t)


def calc(courant, init, pattern_type, timesteps):
    """
    :param courant: критерий Куранта
    :param init: начальные значения
    :param pattern_type: тип шаблона
    :param timesteps: временные шаги
    :return: результат
    """
    u = init
    u_next = np.zeros_like(init)

    if pattern_type == 'UPWIND':
        for j, _ in enumerate(timesteps[:-1]):
            for i in range(1, len(u) - 1):
                u_next[i] = courant * (u[i - 1] - u[i]) + u[i]
            u_next[0] = header.mu(timesteps[j+1])
            u, u_next = u_next, u

    elif pattern_type == 'LAX_WN':
        for j, _ in enumerate(timesteps[:-1]):
            for i in range(1, len(u) - 1):
                u_next[i] = 0.5 * courant**2 * (u[i+1] - 2*u[i] + u[i-1]) - 0.5 * courant * (u[i+1] - u[i-1]) + u[i]
            u_next[0] = header.mu(timesteps[j+1])
            u, u_next = u_next, u

    return u
