import numpy as np

import header


# u_t + a * u_x = 0
# u(x, 0) = phi(x)
# u(0, t) = mu(t)


def flux_limiter(r):
    # van Leer
    return (r + np.abs(r)) / (1 + np.abs(r))

    # van Albada 2
    # return 2*r / (r**2 + 1)


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
            u_next[0] = header.mu(timesteps[j + 1])
            u, u_next = u_next, u

    elif pattern_type == 'LAX_WN':
        for j, _ in enumerate(timesteps[:-1]):
            for i in range(1, len(u) - 1):
                u_next[i] = 0.5 * courant ** 2 * (u[i + 1] - 2 * u[i] + u[i - 1]) - 0.5 * courant * (u[i + 1] - u[i - 1]) + u[i]
            u_next[0] = header.mu(timesteps[j + 1])
            u, u_next = u_next, u

    elif pattern_type == 'LAXTVD':
        for j, _ in enumerate(timesteps[:-1]):
            u_next[0] = header.mu(timesteps[j + 1])
            u_next[1] = 0.5 * courant ** 2 * (u[2] - 2 * u[1] + u[0]) - 0.5 * courant * (u[2] - u[0]) + u[1]
            for i in range(2, len(u) - 1):
                slope1 = (u[i-1] - u[i-2]) / (u[i] - u[i-1]) if u[i] - u[i-1] != 0 else 1
                slope2 = (u[i] - u[i-1]) / (u[i+1] - u[i]) if u[i+1] - u[i] != 0 else 1
                flux1 = u[i-1] + flux_limiter(slope1) * (0.5 * (u[i-1] * (courant + 1) + u[i] * (1 - courant)) - u[i - 1])
                flux2 = u[i] + flux_limiter(slope2) * (0.5 * (u[i] * (courant + 1) + u[i + 1] * (1 - courant)) - u[i])
                u_next[i] = courant * (flux1 - flux2) + u[i]
            u, u_next = u_next, u

    else:
        raise(Exception('No such method'))
    return u
