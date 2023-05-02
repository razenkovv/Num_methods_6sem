import numpy as np

# 2 dimensional heat equation
# u_t = c1*u_xx + c2*u_yy; c1, c2 = const
# x: [x_0, x_1], y: [y_0, y_1] - rectangle region
# t > 0
# u(x,y,0) = f_0(x,y)
# boundary condition - zero gradient

c1 = 0.1
c2 = 5.0

x_0 = 0.0
x_1 = 1.0
y_0 = 0.0
y_1 = 1.0

u_0 = 1.0
r_0 = 0.1
x_c = 0.5
y_c = 0.5


def f_0(mesh_):
    for i in range(n_x):
        for j in range(n_y):
            mesh_[j, i] = np.heaviside(r_0 - (x_c-x_axis[i]) ** 2 - (y_c-y_axis[j]) ** 2, 0) * u_0
    return mesh


h_x = 0.01
h_y = 0.01

t_start = 0.0
t_end = 0.1

frames_per_save = 20

n_x = int((x_1 - x_0) / h_x) + 1
n_y = int((y_1 - y_0) / h_y) + 1
tau = 0.5 / (c1 / h_x**2 + c2 / h_y**2)  # convergence: tau <= 0.5 / (c1/h_x^2 + c2/h_y^2)
mesh = np.zeros((n_y, n_x))
x_axis = np.linspace(x_0, x_1, n_x)
y_axis = np.linspace(y_0, y_1, n_y)
timesteps = np.arange(t_start, t_end, tau)

directory = 'data'

print(f'tau = {tau}')
