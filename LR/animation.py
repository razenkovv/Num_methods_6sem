import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers
import numpy as np

import header

fig, ax = plt.subplots(2, 1, figsize=(16, 8))

data1 = np.genfromtxt(f'data/{header.method}_{header.func}_h=0.01_c={header.courant}.csv', delimiter=',')
print('read')
x1 = data1[0]
data1 = np.delete(data1, 0, axis=0)
data2 = np.genfromtxt(f'data/{header.method}_{header.func}_h=0.001_c={header.courant}.csv', delimiter=',')
print('read')
x2 = data2[0]
data2 = np.delete(data2, 0, axis=0)[::10] #10 - отнощение шагов 0.01 / 0.001

line1 = ax[0].plot(x1, data1[0], label='h=0.01', color='r')[0]
line2 = ax[0].plot(x2, data2[0], label='h=0.001', color='g')[0]
line3 = ax[0].plot(x2, header.exact(x2, 0.0), label='exact', color='b')[0]
ax[0].legend()
ttl1 = ax[0].text(0.4, 1.05, 'Схема Уголок, С=0.7, t=0.00', transform=ax[0].transAxes)

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
    print(frame)
    line1.set_data(x1, data1[frame])
    #line1.set_xdata(x1)
    #line1.set_ydata(data1[frame])
    line2.set_xdata(x2)
    line2.set_ydata(data2[frame])
    line3.set_xdata(x2)
    line3.set_ydata(header.exact(x2, frame * header.tau * header.frames_per_save))
    ttl1.set_text(f'Схема Уголок, С=0.7, t={frame * header.tau * header.frames_per_save:.2f}')

    _error1 = np.max(np.abs(data1[frame] - header.exact(x1, frame * header.tau * header.frames_per_save)))
    _error2 = np.max(np.abs(data2[frame] - header.exact(x2, frame * header.tau * header.frames_per_save)))
    t_axis.append(frame * header.tau * header.frames_per_save)
    error1.append(_error1)
    error2.append(_error2)
    line4.set_xdata(t_axis)
    line4.set_ydata(error1)
    line5.set_xdata(t_axis)
    line5.set_ydata(error2)
    ttl2.set_text(f'Погрешность, отношение={_error1/_error2:.2f}')

    ax[1].set_ylim(0.0, max(_error1, _error2)*1.2)

    return line1, line2, line3, line4, line5, ttl1, ttl2


ani = FuncAnimation(fig=fig, init_func=init, func=update, frames=len(data1), interval=100, repeat=False)
plt.show()

# Writer = writers['ffmpeg']
# writer = Writer(fps=5)
# ani.save('animation.mp4', writer)
