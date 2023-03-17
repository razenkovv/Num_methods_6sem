import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers
import numpy as np
import csv

import header


def leap(r, n):
    res = []
    for i in range(n):
        res = next(r)
    return np.array(res).astype(float)


ratio = int(0.01 / 0.001)  # отношение шагов
if header.h != 0.01:
    print('problems with h')

fig, ax = plt.subplots(2, 1, figsize=(16, 8))

with open(f'data/{header.method}_{header.func}_h=0.01_c={header.courant}_frpersave={header.frames_per_save}.csv', newline='') as f1, \
        open(f'data/{header.method}_{header.func}_h=0.001_c={header.courant}_frpersave={header.frames_per_save}.csv', newline='') as f2:
    frame_number = sum(1 for _ in f1) - 2
    f1.seek(0)
    r1 = csv.reader(f1, delimiter=',')
    r2 = csv.reader(f2, delimiter=',')
    x1 = np.array(next(r1)).astype(float)
    x2 = np.array(next(r2)).astype(float)
    y1 = np.array(next(r1)).astype(float)
    y2 = np.array(next(r2)).astype(float)

    line1 = ax[0].plot(x1, y1, label='h=0.01', color='r')[0]
    line2 = ax[0].plot(x2, y2, label='h=0.001', color='g')[0]
    line3 = ax[0].plot(x1, header.exact(x1, 0.0), label='exact', color='b')[0]
    ax[0].legend()
    ttl1 = ax[0].text(0.4, 1.05, f'Схема {header.method}, С={header.courant}, t=0.00', transform=ax[0].transAxes)

    t_axis = []
    error1 = []
    error2 = []
    line4 = ax[1].plot([], [], color='r', label='h=0.01')[0]
    line5 = ax[1].plot([], [], color='g', label='h=0.001')[0]
    ax[1].legend()
    ttl2 = ax[1].text(0.4, 1.05, 'Погрешность, отношение=', transform=ax[1].transAxes)


    def init():
        ax[1].set_xlim(0.0, 2.0)
        return line1, line2, line3, line4, line5, ttl1, ttl2


    def update(frame):
        frame += 1
        y1 = np.array(next(r1)).astype(float)
        y2 = leap(r2, ratio)
        line1.set_data(x1, y1)
        line2.set_data(x2, y2)
        line3.set_data(x1, header.exact(x1, frame * header.tau * header.frames_per_save))
        ttl1.set_text(f'Схема {header.method}, С={header.courant}, t={frame * header.tau * header.frames_per_save:.2f}')

        _error1 = np.max(np.abs(y1 - header.exact(x1, frame * header.tau * header.frames_per_save)))
        _error2 = np.max(np.abs(y2 - header.exact(x2, frame * header.tau * header.frames_per_save)))
        t_axis.append(frame * header.tau * header.frames_per_save)
        error1.append(_error1)
        error2.append(_error2)
        line4.set_data(t_axis, error1)
        line5.set_data(t_axis, error2)
        ttl2.set_text(f'Погрешность, отношение={_error1 / _error2:.2f}')

        ax[1].relim()
        ax[1].autoscale_view()

        return line1, line2, line3, line4, line5, ttl1, ttl2


    ani = FuncAnimation(fig=fig, init_func=init, func=update, frames=frame_number, interval=1, repeat=False)

    k = 0
    if k:
        plt.show()
    else:
        Writer = writers['ffmpeg']
        writer = Writer(fps=30)
        ani.save(f'animations/{header.method}_{header.func}.mp4', writer)
