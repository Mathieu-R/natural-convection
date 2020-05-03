import numpy as np 
import math

"""
f''' = - 3ff'' + 2(f')^2 - theta
theta'' = - 3 Pr f theta'
"""
def blasius_edo_flow(self, f, theta):
  return np.array([
    f[1], # f' = df/dn
    f[2], # f'' = d^2f/dn^2
    - 3 * f[1] * f[2] + 2 * math.pow(f[1], 2) - theta[0] # f''' = - 3ff'' + 2(f')^2 - theta
  ])

def blasius_edo_heat(self, f, theta):
  return np.array([
    theta[1], # theta' = dtheta/dn
    - 3 * self.Prandtl * f[0] * theta[1] # theta'' = - 3 Pr f theta'
  ])