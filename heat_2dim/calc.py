import numpy as np
import os
import shutil

import header


def calc_explicit(frames_per_save=header.frames_per_save, mesh=header.mesh, timesteps=header.timesteps, startmark=0, u_0=np.nan):
    """
    :param frames_per_save: частота записи
    :param mesh: сетка (двумерный массив)
    :param timesteps: шаги по времени
    :param startmark: если не равен 0, то используются значения u_0
    :param u_0: значения в момент времени timesteps[0]
    :return: значения в момент времени timesteps[-1]
    """

    if os.path.exists(header.directory):
        raise Exception(f'Delete or rename subdirectory {header.directory}')
    os.mkdir(f'{header.directory}')

    if not os.path.exists('description'):
        os.mkdir('description')
    shutil.copy('header.py', 'description/description.txt')

    if startmark == 0:
        u_0 = header.f_0(mesh)

    np.savetxt(f'{header.directory}/{timesteps[0]}.csv', u_0, delimiter=',')

    u_1 = np.zeros_like(u_0)

    i = int(0)

    for _ in timesteps[:-1]:
        i += 1
        u_1[1:-1, 1:-1] = u_0[1:-1, 1:-1] + header.c1 * header.tau / header.h_x ** 2 * (
                    u_0[2:, 1:-1] - 2 * u_0[1:-1, 1:-1] + u_0[:-2, 1:-1]) + header.c2 * header.tau / header.h_y ** 2 * (u_0[1:-1, 2:] - 2 * u_0[1:-1, 1:-1] + u_0[1:-1, :-2])
        u_1[:1, :] = u_1[1:2, :]
        u_1[-1:, :] = u_1[-2:-1, :]
        u_1[:, :1] = u_1[:, 1:2]
        u_1[:, -1:] = u_1[:, -2:-1]

        u_0, u_1 = u_1, u_0

        if i % frames_per_save == 0:
            np.savetxt(f'{header.directory}/{timesteps[i]}.csv', u_0, delimiter=',')
            print(timesteps[i])

    return u_0
