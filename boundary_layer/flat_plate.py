import numpy as np

# We consider a vertical plate
class plate():
  """
  length: length of the plate
  t_wall: temperature on the plate wall
  eta_max: distance max to the plate (to evaluate stuff)

  """
  def __init__(self, length, t_wall, eta_max):
    self.L = length
    self.Tw = t_wall
    self.eta_max = eta_max
    self.eta_range = np.linspace(0, eta_max, 500)

  def mesh(self, delta_estimated, ue, nu):
    n_x = 500
    n_y = 500

    self.x = self.L * np.logspace(-5,0, n_x + 1)
    self.y = np.linspace(0,50 * delta_estimated, n_y + 1)

    self.eta = np.linspace(0, 6, n_x+1)

    self.X, self.Y = np.meshgrid(self.x, self.y)

    # dimensionless similarity variable
    #self.eta_similarity = ((ue / (2 * nu * self.X)) ** 0.5) * self.Y
