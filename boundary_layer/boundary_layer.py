import numpy as np

from scipy.integrate import solve_bvp

class boundary_layer():
  def __init__(self, stream, plate, Pr):
    self.T_w = 0
    self.T_e = 0
    self.deltaT = self.T_w - self.T_e

    # Prandtl
    self.Pr = Pr

    # Nusselt
    self.Nusselt = []

    self.stream = stream
    self.plate = plate

    self.solve()

  def solve(self):

    def similitude_ode(x, y, parameters):
      # y = [f, f', f'', theta, theta']
      #      0  1    2     3      4

      Pr = parameters[0]

      return np.array([
        # flow edo
        y[1], # f' = df/dn
        y[2], # f'' = d^2f/dn^2
        - 3 * y[0] * y[2] + (2 * (y[1]**2)) - y[3], # f''' = - 3ff'' + 2(f')^2 - theta,
        # heat edo
        y[4], # theta' = dtheta/dn
        - 3 * Pr * y[0] * y[4], # theta'' = - 3 Pr f theta'
      ])

    def boundary_conditions(ya, yb, parameters):
      # ya = y(eta = 0)
      # yb = y(eta -> infty)

      # f(0) = 0 ; f'(0) = 0 ; theta(0) = 1
      # f'(infty) = 0 ; theta(infty) = 0
      return np.array([ya[0], ya[1], ya[3] - 1, yb[1], yb[3]])

    self.plate.generate_discrete_space()
    self.result = solve_bvp(fun=similitude_ode, bc=boundary_conditions, x=self.plate.x_mesh, y=self.plate.u, p=[self.Pr])



