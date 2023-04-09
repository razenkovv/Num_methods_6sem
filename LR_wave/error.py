import pandas as pd
import numpy as np
from tabulate import tabulate
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

import header
import calc

hsteps = [0.05 * 0.5 ** k for k in range(8)]
#hsteps = [0.01, 0.001]
df = pd.DataFrame(index=range(len(hsteps)), columns=['h', 'error'])

for j, h in enumerate(hsteps):
    tau = header.courant * h / np.sqrt(header.c)
    mesh = np.arange(header.lft, header.rgt, h)
    timesteps = np.arange(header.t_start, header.t_end, tau)
    calc.calc_without_writing()


# df.iloc[j] = h, error
# df = pd.read_csv(f'graphs/errors_{header.method}_{header.func}_c={header.courant}.csv', index_col=0)

model = LinearRegression().fit(np.log(df['h'].to_numpy(dtype=float)).reshape(-1, 1), np.log(df['error'].to_numpy(dtype=float)))
df.plot(figsize=(8, 8), x='h', y='error', loglog=True, marker='P', title=f'Errors_{header.method}_c={header.courant}')
plt.text(0.7, 0.1, f'mean_tan={model.coef_[0]:.3f}', transform=plt.gca().transAxes)

k = 1
if k:
    print(f'{header.method}')
    print(f'mean_tan = {model.coef_[0]:.3f}')
    print(tabulate(df, headers=['h', 'error'], tablefmt='github'))
    plt.show()
else:
    plt.savefig(f'graphs/Errors_{header.method}_c={header.courant}.png')
    df.to_csv(f'graphs/Errors_{header.method}_c={header.courant}.csv')
