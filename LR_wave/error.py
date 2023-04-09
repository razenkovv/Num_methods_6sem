import pandas as pd
import numpy as np
from tabulate import tabulate
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

import header
import calc

hsteps = [0.05 * 0.5 ** k for k in range(8)]
df = pd.DataFrame(index=range(len(hsteps)), columns=['h', 'error'])

for j, h in enumerate(hsteps):
    mesh = np.linspace(header.lft, header.rgt, int((header.rgt - header.lft) / h) + 1)
    timesteps = np.arange(header.t_start, header.t_end, header.courant * h / np.sqrt(header.c))
    errors = np.zeros_like(timesteps)
    u_0, u_1 = calc.calc_without_writing(mesh, timesteps[0:2], pattern_type=header.method)
    errors[1] = header.error_estimation(u_1 - header.exact(mesh, timesteps[1]))

    for i, t in enumerate(timesteps[1:-1]):
        u_0, u_1 = calc.calc_without_writing(mesh, timesteps[i:i+3], pattern_type=header.method, startmark=1, u_0=u_0, u_1=u_1)
        errors[i+2] = header.error_estimation(u_1 - header.exact(mesh, timesteps[i+2]))
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
