import numpy as np
import math

from .shooting import shooting

class boundary_layer():
  def __init__(self, stream, plate, Pr):
    # initial conditions
    self.f0 = [0, 0, 0]
    self.theta0 = [1, 0]
    self.initial_values = self.f0 + self.theta0

    # boundary conditions
    self.finf = [0, 0, 0]
    self.thetainf = [0, 0]
    self.boundary_values = self.finf + self.thetainf

    # guesses
    self.f_guesses = {
      "guesses": [1e-2, 2],
      "guess_position": 2, # f''(0)
      "boundary_position": 1 # f'(eta -> infty)
    }

    self.theta_guesses = {
      "guesses": [-0,1, 0,1],
      "guess_position": 4, # theta'(0)
      "boundary_position": 3 # theta(eta -> infty)
    }

    self.T_w = 0
    self.T_e = 0
    self.deltaT = self.T_w - self.T_e

    # results
    self.f = []
    self.df = []
    self.ddf = []

    self.theta = []
    self.dtheta = []

    # Prandtl
    self.Pr = Pr

    # Nusselt
    self.Nusselt = []

    self.stream = stream
    self.plate = plate

    self.solve()

  def similitude_ode(self, t, y, Pr):
    # y = [f, f', f'', theta, theta']
    #      0  1    2     3      4
    return np.array([
      # flow edo
      y[1], # f' = df/dn
      y[2], # f'' = d^2f/dn^2
      - 3 * y[0] * y[2] + (2 * (y[1]**2)) - y[3], # f''' = - 3ff'' + 2(f')^2 - theta,
      # heat edo
      y[4], # theta' = dtheta/dn
      - 3 * Pr * y[0] * y[4], # theta'' = - 3 Pr f theta'
    ])

  def compute_interesting_values(self):
    #self.delta =
    #self.delta_start =
    #self.Gr = (beta * self.deltaT * self.g * (y**3)) / (self.nu ** 2)
    #self.qw = -k * self.deltaT * self.f[0, 4] * (1 / y)
    #self.Nusselt =
    pass

  def solve(self):
    # two boundary values = two guess at the same time
    guesses = [self.f_guesses, self.theta_guesses]

    shoot = shooting(
      ode=self.similitude_ode, initial_values=self.initial_values, boundary_values=self.boundary_values,
      t_range=self.plate.eta_range, guesses=guesses, args=(self.Pr,)
    )

    y = shoot.shoot()
    self.f = y[:, 0]
    self.df = y[:, 1]
    self.ddf = y[:, 2]

    self.theta = y[:, 3]
    self.dtheta = y[:, 4]

    self.compute_interesting_values()
