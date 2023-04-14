import numpy as np
import csv

import header


def calc_with_writing(pattern_type, path, frames_per_save, mesh=header.mesh, timesteps=header.timesteps, startmark=0, u_0=np.nan):
    """
    :param pattern_type: метод
    :param path: файл для записи
    :param frames_per_save: частота записи
    :param mesh: сетка
    :param timesteps: шаги по времени
    :param startmark: если не равен 0, то используются значения u_0
    :param u_0: значения в момент времени timesteps[0]
    :return: значения в момент времени timesteps[-1]
    """
    with open(path, 'w', newline='') as f:

        if startmark == 0:
            u_0 = header.f_0(mesh)
        u_1 = np.zeros_like(u_0)

        csv.writer(f, delimiter=',').writerow(mesh)
        csv.writer(f, delimiter=',').writerow(timesteps[::frames_per_save])
        csv.writer(f, delimiter=',').writerow(u_0)
        i = int(0)

        for t in timesteps[:-1]:
            i += 1
            left, right = make_system(pattern_type, u_0, t, mesh, timesteps)
            u_1 = tdma(left, right)
            u_0, u_1 = u_1, u_0
            if i % frames_per_save == 0:
                csv.writer(f, delimiter=',').writerow(u_0)

    return u_0


def calc_without_writing(pattern_type, mesh=header.mesh, timesteps=header.timesteps, startmark=0, u_0=np.nan):
    """
    :param pattern_type: метод
    :param mesh: сетка
    :param timesteps: шаги по времени
    :param startmark: если не равен 0, то используются значения u_0
    :param u_0: значения в момент времени timesteps[0]
    :return: значения в момент времени timesteps[-1]
    """

    if startmark == 0:
        u_0 = header.f_0(mesh)
    u_1 = np.zeros_like(u_0)

    for i, t in enumerate(timesteps[:-1]):
        left, right = make_system(pattern_type, u_0, t, mesh, timesteps)
        u_1 = tdma(left, right)
        u_0, u_1 = u_1, u_0

    return u_0


def make_system(pattern_type, u_0, t, mesh, timesteps):
    n = 3
    left = np.zeros((len(mesh) - 2) * n + 4)
    right = np.zeros_like(mesh)
    h = mesh[1] - mesh[0]
    tau = timesteps[1] - timesteps[0]

    left[n - 1:-2:n] = header.courant * header.sigma
    left[n:-1:n] = -2 * header.courant * header.sigma - 1
    left[n + 1::n] = header.courant * header.sigma
    right[1:-1] = -u_0[1:-1] - tau * header.f(mesh, t + 0.5 * tau)[1:-1] + (header.sigma - 1) * header.courant * (u_0[2:] - 2 * u_0[1:-1] + u_0[:-2])

    if pattern_type == 'WEIGHT_1':
        left[0] = -header.a2 / h + header.a1
        left[1] = header.a2 / h
        right[0] = header.f_lft(t + tau)
        left[-2] = -header.b2 / h
        left[-1] = header.b2 / h + header.b1
        right[-1] = header.f_rgt(t + tau)

    elif pattern_type == 'WEIGHT_2':
        if header.a2 != 0:
            left[0] = 1 - 2 * header.courant * header.sigma * (h * header.a1 / header.a2 - 1)
            left[1] = -2 * header.courant * header.sigma
            right[0] = u_0[0] + tau * header.f(mesh[0], t + 0.5 * tau) + header.courant * (-2 * header.sigma * h * header.f_lft(t + tau) / header.a2 + (1 - header.sigma) * (
                    u_0[1] - 2 * u_0[0] - (-2 * h * header.a1 * u_0[0] + 2 * h * header.f_lft(t + tau) - header.a2 * u_0[1]) / header.a2))
        else:
            left[0] = header.a1
            left[1] = 0.0
            right[0] = header.f_lft(t + tau)

        if header.b2 != 0:
            left[-1] = 1 + 2 * header.courant * header.sigma * (1 + h * header.b1 / header.b2)
            left[-2] = -2 * header.courant * header.sigma
            right[-1] = u_0[-1] + tau * header.f(mesh[-1], t + 0.5 * tau) + header.courant * (2 * header.sigma * h * header.f_rgt(t + tau) / header.b2 + (1 - header.sigma) * (
                    -2 * u_0[-1] + u_0[-2] + (-2 * h * header.b1 * u_0[-1] + 2 * h * header.f_rgt(t + tau) + header.b2 * u_0[-2]) / header.b2))
        else:
            left[-1] = header.b1
            left[-2] = 0.0
            right[-1] = header.f_rgt(t + tau)

    else:
        raise Exception("make_system: only 1st or 2nd order")

    return left, right


def tdma(left, right):
    """
    TriDiagonal Matrix Algorithm\n
    Решение СЛАУ с трехдиагональной матрицей. Важно диагональное преобладание.\n
    :param left: массив значений в левой части матрицы (все ненулевые элементы подряд построчно)
    :param right: правая часть матрицы
    :return: массив решений
    """
    n = 3
    if len(left) != (len(right) - 2) * n + 4:
        raise Exception("tdma method: something wrong with input\n")
    a_coef = np.zeros(len(right))
    b_coef = np.zeros(len(right))
    a_coef[0] = right[0] / left[0]
    b_coef[0] = -1 * left[1] / left[0]
    ind = n
    for i in range(1, len(right) - 1):
        a_coef[i] = (right[i] - left[ind - 1] * a_coef[i - 1]) / (left[ind] + left[ind - 1] * b_coef[i - 1])
        b_coef[i] = -1 * left[ind + 1] / (left[ind] + left[ind - 1] * b_coef[i - 1])
        ind += n
    a_coef[-1] = (right[-1] - left[ind - 1] * a_coef[-2]) / (left[ind] + left[ind - 1] * b_coef[-2])
    b_coef[-1] = 0.0

    res = np.zeros(len(right))
    res[-1] = a_coef[-1]
    for i in range(len(res) - 2, -1, -1):
        res[i] = a_coef[i] + b_coef[i] * res[i + 1]
    return res
