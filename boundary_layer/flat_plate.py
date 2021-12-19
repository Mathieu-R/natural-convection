import numpy as np

MESH_POINTS = 500

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
    self.eta_range = np.linspace(0, eta_max, MESH_POINTS)

  def generate_discrete_space(self):
    """Discretize the space of the flat plate. We are in the space (x, y) = (eta, L)
    """

    # flat plate size
    width = self.eta_max
    height = self.L

    # space intervals
    d_eta = dL = 0.05

    # number of steps
    n_eta = int(width/d_eta)
    nL = int(height/dL)

    # mesh points in space
    self.x_mesh = np.linspace(start=0, stop=self.eta_max, num=n_eta+1)
    self.y_mesh = np.linspace(start=0, stop=self.L, num=nL+1)

    # 5 equations so 5 lines
    self.u = np.zeros((5, self.x_mesh.size))

  def mesh(self, delta_estimated, ue, nu):
    n_x = MESH_POINTS
    n_y = MESH_POINTS

    self.x = self.L * np.logspace(-5, 0, n_x + 1)
    self.y = np.linspace(0, 50 * delta_estimated, n_y + 1)

    self.eta = np.linspace(0, 6, n_x+1)

    self.X, self.Y = np.meshgrid(self.x, self.y)

    # dimensionless similarity variable
    #self.eta_similarity = ((ue / (2 * nu * self.X)) ** 0.5) * self.Y
