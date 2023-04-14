import pandas as pd
import numpy as np
from tabulate import tabulate
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

import header
import calc

hsteps = [0.01 * 0.5 ** k for k in range(6)]
print(hsteps)
df = pd.DataFrame(index=range(len(hsteps)), columns=['h', 'error'])

for j, h in enumerate(hsteps):
    print(h)
    mesh = np.linspace(header.lft, header.rgt, int((header.rgt - header.lft) / h) + 1)
    timesteps = np.arange(header.t_start, header.t_end, header.courant * h**2 / header.c)
    errors = np.zeros_like(timesteps)
    u_0 = header.f_0(mesh)

    for i, t in enumerate(timesteps[:-1]):
        u_0 = calc.calc_without_writing(pattern_type=header.method, mesh=mesh, timesteps=timesteps[i:i+2], startmark=1, u_0=u_0)
        errors[i+1] = header.error_estimation(u_0 - header.exact(mesh, timesteps[i+1]))
    error = header.error_estimation(errors)
    df.iloc[j] = h, error


model = LinearRegression().fit(np.log(df['h'].to_numpy(dtype=float)).reshape(-1, 1), np.log(df['error'].to_numpy(dtype=float)))
df.plot(figsize=(8, 8), x='h', y='error', loglog=True, marker='P', title=f'Errors_{header.method}_c={header.courant}')
plt.text(0.7, 0.1, f'mean_tan={model.coef_[0]:.3f}', transform=plt.gca().transAxes)

k = 0
if k:
    print(f'{header.method}')
    print(f'mean_tan = {model.coef_[0]:.3f}')
    print(tabulate(df, headers=['h', 'error'], tablefmt='github'))
    plt.show()
else:
    plt.savefig(f'graphs/Errors_{header.method}_c={header.courant}.png')
    df.to_csv(f'graphs/Errors_{header.method}_c={header.courant}.csv')