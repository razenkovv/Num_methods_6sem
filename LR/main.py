import numpy as np
import csv

import header
from calc import calc

init = header.phi(np.arange(header.x_min, header.x_max, header.h))

# в первой строке записывается x_axis
with open(f'data/{header.method}_{header.func}_h={header.h}_c={header.courant}.csv', 'w', newline='') as f:
    res = init
    csv.writer(f, delimiter=',').writerow(np.arange(header.x_min, header.x_max, header.h))
    csv.writer(f, delimiter=',').writerow(res)
    timesteps = np.arange(header.t_start, header.t_max, header.tau)
    for i, _ in enumerate(timesteps[:-1*header.frames_per_save:header.frames_per_save]):
        res = calc(header.courant, res, header.Method.UPWIND.name, timesteps[i*header.frames_per_save:(i+1)*header.frames_per_save+1])
        csv.writer(f, delimiter=',').writerow(res)
