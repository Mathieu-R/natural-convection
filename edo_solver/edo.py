import numpy as np
import math

"""
  f''' + ff'' = 0
"""
def basic_blasius_edo(t, f):
  return np.array([
    f[1],
    f[2],
    - f[0] * f[2]
  ])

"""
y = [f, f', f'', theta, theta']
dy/dn = [f', f'', f''', theta', theta'']

after integration we get back :
y = [f, f', f'', theta, theta']

with :
f''' = - 3ff'' + 2(f')^2 - theta
theta'' = - 3 Pr f theta'

boundary conditions :
f(0) = 0 ; f'(0) = 0
f'(eta -> infty) = 0

theta(0) = 1
theta(eta -> infty) = 0
"""
def blasius_edo(t, y, prandtl):
  f = y[0:3]
  theta = y[3:5]
  return np.array([
    # flow edo
    y[1], # f' = df/dn
    y[2], # f'' = d^2f/dn^2
    - 3 * y[0] * y[2] + (2 * math.pow(f[1], 2)) - y[3], # f''' = - 3ff'' + 2(f')^2 - theta,
    # heat edo
    y[4], # theta' = dtheta/dn
    - 3 * prandtl * y[0] * y[4], # theta'' = - 3 Pr f theta'
  ])
