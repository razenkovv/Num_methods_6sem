import pandas as pd
import numpy as np
from tabulate import tabulate
from matplotlib import pyplot as plt

import header
from calc import calc


def error_estimation(e):
    # return np.max(np.abs(e))
    # return np.mean(np.abs(e))
    return np.sqrt(sum(e**2)/len(e))


hsteps = [0.1*0.5**k for k in range(10)]

df = pd.DataFrame(index=range(len(hsteps)), columns=['h', 'error'])
for j, h in enumerate(hsteps):
    print(h)
    x_axis = np.arange(header.x_min, header.x_max, h)
    init = header.phi(x_axis)
    res = init
    timesteps = np.arange(header.t_start, header.t_max, header.courant * h / header.speed)
    errors = np.zeros(len(timesteps) - 1)
    for i, _ in enumerate(timesteps[:-1]):
        res = calc(header.courant, res, header.method, timesteps[i:i+2])
        f_exact = header.exact(x_axis, timesteps[i+1])
        errors[i] = error_estimation(res - f_exact)
    df.iloc[j] = h, error_estimation(errors)


# df = pd.read_csv(f'graphs/errors_{header.method}_{header.func}_c={header.courant}.csv', index_col=0)

mean_tan = np.mean(np.log(df['error'].astype(float))/np.log(df['h'].astype(float)))
df.plot(x='h', y='error', loglog=True, marker='P', title=f'Errors_{header.method}_{header.func}_c={header.courant}')
plt.text(0.7, 0.1, f'mean_tan={mean_tan:.3f}', transform=plt.gca().transAxes)

k = 0
if k:
    print(tabulate(df, headers=['h', 'error'], tablefmt='github'))
    plt.show()
else:
    plt.savefig(f'graphs/Errors_{header.method}_{header.func}_c={header.courant}.png')
    df.to_csv(f'graphs/Errors_{header.method}_{header.func}_c={header.courant}.csv')
