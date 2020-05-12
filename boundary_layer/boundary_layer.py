import numpy as np
import math

from .shooting import shooting

class boundary_layer():
  def __init__(self, stream, plate, Pr):
    # initial conditions
    self.f0 = [0, 0, 0]
    self.theta0 = [1, 0]

    # boundary conditions
    self.finf = [0, 0, 0]
    self.thetainf = [0, 0]

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

  def flow_ode(self, t, f, theta):
    return np.array([
      f[1],
      f[2],
      -3 * f[0] * f[2] + (2 * (f[1]**2)) - theta[0]
    ])

  def heat_ode(self, t, theta, f, Pr):
    return np.array([
      theta[1],
      -3 * Pr * f[0] * theta[1]
    ])

  def similitude_ode(self, t, y, Pr):
    return np.array([
      # flow edo
      y[1], # f' = df/dn
      y[2], # f'' = d^2f/dn^2
      - 3 * y[0] * y[2] + (2 * math.pow(f[1], 2)) - y[3], # f''' = - 3ff'' + 2(f')^2 - theta,
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
    shoot = shooting(
      ode=self.flow_ode, initial_values=self.f0, boundary_values=self.finf, t_range=self.plate.eta_range,
      guesses=[1e-2, 2], guess_position=2, boundary_position=1,
      args=(self.theta0,)
    )

    f = shoot.shoot()
    self.f = f[:, 0]
    self.df = f[:, 1]
    self.ddf = f[:, 2]

    shoot = shooting(
      ode=self.heat_ode, initial_values=self.theta0, boundary_values=self.thetainf, t_range=self.plate.eta_range,
      guesses=[-0.1, 0.1], guess_position=1, boundary_position=0,
      args=(self.f0, self.Pr,)
    )

    theta = shoot.shoot()
    self.theta = theta[:, 0]
    self.dtheta = theta[:, 1]

    self.compute_interesting_values()
