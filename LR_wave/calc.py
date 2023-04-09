import numpy as np
import csv

import header


def calc_with_writing(mesh, timesteps, pattern_type, path, frames_per_save, startmark=0, u_0=np.nan, u_1=np.nan):
    """
    :param mesh: сетка
    :param timesteps: шаги по времени
    :param pattern_type: метод
    :param path: файл для записи
    :param frames_per_save: частота записи
    :param startmark: если не равен 0, то используются значения u_0 и u_1
    :param u_0: значения в момент времени timesteps[0]
    :param u_1: значения в момент времени timesteps[1]
    :return: значения в момент времени timesteps[-2] и timesteps[-1]
    """
    with open(path, 'w', newline='') as f:

        tau = timesteps[1] - timesteps[0]
        h = mesh[1] - mesh[0]
        if startmark == 0:
            u_0 = header.f_0(mesh)
        u_2 = np.zeros_like(u_0)

        csv.writer(f, delimiter=',').writerow(mesh)
        csv.writer(f, delimiter=',').writerow(timesteps[::frames_per_save])
        csv.writer(f, delimiter=',').writerow(u_0)
        i = int(1)

        if pattern_type == 'CROSS_1':
            if startmark == 0:
                u_1 = u_0 + header.f_0t(mesh) * tau
            if i % frames_per_save == 0:
                csv.writer(f, delimiter=',').writerow(u_1)
            for t in timesteps[1:-1]:
                i += 1
                u_2[1:-1] = (u_1[2:] - 2 * u_1[1:-1] + u_1[:-2]) * header.c * tau ** 2 / h ** 2 + header.f(mesh[1:-1], t) * tau ** 2 + 2 * u_1[1:-1] - u_0[1:-1]
                u_2[0] = (header.f_lft(t + tau) * h - header.a2 * u_2[1]) / (header.a1 * h - header.a2)
                u_2[-1] = (header.f_rgt(t + tau) * h + header.b2 * u_2[-2]) / (header.b1 * h + header.b2)
                u_0, u_1, u_2 = u_1, u_2, u_0
                if i % frames_per_save == 0:
                    csv.writer(f, delimiter=',').writerow(u_1)

        elif pattern_type == 'CROSS_2':
            if startmark == 0:
                u_1 = u_0 + header.f_0t(mesh) * tau + (header.c * header.f_0xx(mesh) + header.f(mesh, 0.0)) * 0.5 * tau ** 2
            if i % frames_per_save == 0:
                csv.writer(f, delimiter=',').writerow(u_1)
            for t in timesteps[1:-1]:
                i += 1
                u_2[1:-1] = (u_1[2:] - 2 * u_1[1:-1] + u_1[:-2]) * header.c * tau ** 2 / h ** 2 + header.f(mesh[1:-1], t) * tau ** 2 + 2 * u_1[1:-1] - u_0[1:-1]
                u_2[0] = (header.f_lft(t + tau) * h - 2 * header.a2 * u_2[1] + 0.5 * header.a2 * u_2[2]) / (header.a1 * h - 1.5 * header.a2)
                u_2[-1] = (header.f_rgt(t + tau) * h + 2 * header.b2 * u_2[-2] - 0.5 * header.b2 * u_2[-3]) / (header.b1 * h + 1.5 * header.b2)
                u_0, u_1, u_2 = u_1, u_2, u_0
                if i % frames_per_save == 0:
                    csv.writer(f, delimiter=',').writerow(u_1)

        else:
            raise (Exception('No such method'))

        return u_0, u_1


def calc_without_writing(mesh, timesteps, pattern_type, startmark=0, u_0=np.nan, u_1=np.nan):
    """
        :param mesh: сетка
        :param timesteps: шаги по времени
        :param pattern_type: метод
        :param startmark: если не равен 0, то используются значения u_0 и u_1
        :param u_0: значения в момент времени timesteps[0]
        :param u_1: значения в момент времени timesteps[1]
        :return: значения в момент времени timesteps[-2] и timesteps[-1]
        """

    errors_ = np.zeros(len(timesteps - 1))

    tau = timesteps[1] - timesteps[0]
    h = mesh[1] - mesh[0]
    if startmark == 0:
        u_0 = header.f_0(mesh)
    u_2 = np.zeros_like(u_0)

    if pattern_type == 'CROSS_1':
        if startmark == 0:
            u_1 = u_0 + header.f_0t(mesh) * tau
        errors_[0] = header.error_estimation(u_1 - header.exact(mesh, timesteps[1]))
        for t in timesteps[1:-1]:
            u_2[1:-1] = (u_1[2:] - 2 * u_1[1:-1] + u_1[:-2]) * header.c * tau ** 2 / h ** 2 + header.f(mesh[1:-1], t) * tau ** 2 + 2 * u_1[1:-1] - u_0[1:-1]
            u_2[0] = (header.f_lft(t + tau) * h - header.a2 * u_2[1]) / (header.a1 * h - header.a2)
            u_2[-1] = (header.f_rgt(t + tau) * h + header.b2 * u_2[-2]) / (header.b1 * h + header.b2)
            errors_[int(t/tau)] = header.error_estimation(u_2 - header.exact(mesh, t))
            u_0, u_1, u_2 = u_1, u_2, u_0

    elif pattern_type == 'CROSS_2':
        if startmark == 0:
            u_1 = u_0 + header.f_0t(mesh) * tau + (header.c * header.f_0xx(mesh) + header.f(mesh, 0.0)) * 0.5 * tau ** 2
        errors_[0] = header.error_estimation(u_1 - header.exact(mesh, timesteps[1]))
        for t in timesteps[1:-1]:
            u_2[1:-1] = (u_1[2:] - 2 * u_1[1:-1] + u_1[:-2]) * header.c * tau ** 2 / h ** 2 + header.f(mesh[1:-1], t) * tau ** 2 + 2 * u_1[1:-1] - u_0[1:-1]
            u_2[0] = (header.f_lft(t + tau) * h - 2 * header.a2 * u_2[1] + 0.5 * header.a2 * u_2[2]) / (header.a1 * h - 1.5 * header.a2)
            u_2[-1] = (header.f_rgt(t + tau) * h + 2 * header.b2 * u_2[-2] - 0.5 * header.b2 * u_2[-3]) / (header.b1 * h + 1.5 * header.b2)
            errors_[int(t / tau)] = header.error_estimation(u_2 - header.exact(mesh, t))
            u_0, u_1, u_2 = u_1, u_2, u_0

    else:
        raise (Exception('No such method'))

    return u_0, u_1, header.error_estimation(errors_)
