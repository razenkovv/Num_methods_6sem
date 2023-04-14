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


steps = (0.01, 0.001)

ratio = int(steps[0] / steps[1])**2 # отношение шагов; в квадрате так как tau ~ h**2

if header.h != steps[0]:
    raise Exception(f'Animation: for correct working header.h must be {steps[0]}')

fig, ax = plt.subplots(2, 1, figsize=(16, 8))

with open(f'data/{header.method}_h={steps[0]}_c={header.courant}_frpersave={header.frames_per_save}.csv', newline='') as f1, \
        open(f'data/{header.method}_h={steps[1]}_c={header.courant}_frpersave={header.frames_per_save}.csv', newline='') as f2:
    frame_number = sum(1 for _ in f1) - 3
    f1.seek(0)
    r1 = csv.reader(f1, delimiter=',')
    r2 = csv.reader(f2, delimiter=',')
    x1 = np.array(next(r1)).astype(float)
    x2 = np.array(next(r2)).astype(float)
    next(r1)  # пропускаем timesteps
    next(r2)
    y1 = np.array(next(r1)).astype(float)
    y2 = np.array(next(r2)).astype(float)

    line1 = ax[0].plot(x1, y1, label=f'h={steps[0]}', color='r')[0]
    line2 = ax[0].plot(x2, y2, label=f'h={steps[1]}', color='g')[0]
    line3 = ax[0].plot(x1, header.exact(x1, 0.0), label='exact', color='b')[0]
    ax[0].legend()
    ttl1 = ax[0].text(0.4, 1.05, f'Схема {header.method}, С={header.courant}, t=0.00', transform=ax[0].transAxes)

    t_axis = []
    error1 = []
    error2 = []
    line4 = ax[1].plot([], [], color='r', label=f'h={steps[0]}')[0]
    line5 = ax[1].plot([], [], color='g', label=f'h={steps[1]}')[0]
    ax[1].legend()
    ttl2 = ax[1].text(0.4, 1.05, 'Погрешность, отношение=', transform=ax[1].transAxes)


    def init():
        ax[1].set_xlim(header.t_start, header.t_end)
        return line1, line2, line3, line4, line5, ttl1, ttl2


    def update(frame):
        frame += 1
        y1 = np.array(next(r1)).astype(float)
        y2 = leap(r2, ratio)
        line1.set_data(x1, y1)
        line2.set_data(x2, y2)
        line3.set_data(x1, header.exact(x1, frame * header.tau * header.frames_per_save))
        ttl1.set_text(f'Схема {header.method}, С={header.courant}, t={frame * header.tau * header.frames_per_save:.2f}')

        _error1 = header.error_estimation(y1 - header.exact(x1, frame * header.tau * header.frames_per_save))
        _error2 = header.error_estimation(y2 - header.exact(x2, frame * header.tau * header.frames_per_save))
        t_axis.append(frame * header.tau * header.frames_per_save)
        error1.append(_error1)
        error2.append(_error2)
        line4.set_data(t_axis, error1)
        line5.set_data(t_axis, error2)
        ttl2.set_text(f'Погрешность, отношение={_error1 / _error2:.2f}')

        ax[0].relim()
        ax[0].autoscale_view()
        ax[1].relim()
        ax[1].autoscale_view()

        return line1, line2, line3, line4, line5, ttl1, ttl2


    ani = FuncAnimation(fig=fig, init_func=init, func=update, frames=frame_number, interval=1, repeat=False)

    k = 0
    if k:
        plt.show()

    else:
        Writer = writers['ffmpeg']
        writer = Writer(fps=20)
        ani.save(f'animations/{header.method}.mp4', writer)