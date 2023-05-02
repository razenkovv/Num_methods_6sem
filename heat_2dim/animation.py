import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation, writers
import numpy as np
import os

import header

files = os.listdir(f'{header.directory}')
files = [float(os.path.splitext(f)[0]) for f in files]
files.sort()
files = [str(f) + '.csv' for f in files]


def init():
    pass


def update(frame):
    print(frame)
    ax.axis('off')
    ax.set_title(f't={float(os.path.splitext(files[frame])[0]):.3f}')
    u = np.genfromtxt(f'{header.directory}/{files[frame]}', delimiter=',')
    sns.heatmap(u, ax=ax, cbar=True, cbar_ax=cax, vmin=0.0, vmax=1.0, cmap='jet')


grid_kws = {'width_ratios': (0.9, 0.05), 'wspace': 0.2}
fig, (ax, cax) = plt.subplots(1, 2, gridspec_kw=grid_kws, figsize=(10, 8))
ani = FuncAnimation(fig=fig, init_func=init, func=update, frames=len(files), interval=1, repeat=False)

k = 0
if k:
    plt.show()
else:
    Writer = writers['ffmpeg']
    writer = Writer(fps=25)
    if not os.path.exists('animations'):
        os.mkdir('animations')
    ani.save(f'animations/task.mp4', writer)
