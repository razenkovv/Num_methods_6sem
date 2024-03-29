import numpy as np
import csv

import header
from calc import calc

init = header.phi(np.arange(header.x_min, header.x_max, header.h))

# в первой строке записывается x_axis
with open(f'data/{header.method}_{header.func}_h={header.h}_c={header.courant}_frpersave={header.frames_per_save}.csv', 'w', newline='') as f:
    res = init
    csv.writer(f, delimiter=',').writerow(np.arange(header.x_min, header.x_max, header.h))
    csv.writer(f, delimiter=',').writerow(res)
    timesteps = np.arange(header.t_start, header.t_max, header.tau)
    load_bar = 0
    print(load_bar, '%')
    for i, _ in enumerate(timesteps[:-1*header.frames_per_save:header.frames_per_save]):
        if int(100 * header.frames_per_save * i / len(timesteps)) != load_bar:
            load_bar = int(100 * header.frames_per_save * i / len(timesteps))
            print(load_bar, '%')
        res = calc(header.courant, res, header.method, timesteps[i*header.frames_per_save:(i+1)*header.frames_per_save+1])
        csv.writer(f, delimiter=',').writerow(res)
    print(100, '%')
