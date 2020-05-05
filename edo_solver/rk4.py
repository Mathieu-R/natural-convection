import numpy as np
import matplotlib.pyplot as plt

from .solver import EDONumericalResolution

class RK4Method(EDONumericalResolution):
  # notice time is not present in this case.
  # we don't need it in the numerical solutions.
  def derivatives(self, y):
    k1 = self.edo(self, y)
    k2 = self.edo(self, y + ((self.time_step / 2) * k1))
    k3 = self.edo(self, y + ((self.time_step / 2) * k2))
    k4 = self.edo(self, y + (self.time_step * k3))
    return (k1 + 2*k2 + 2*k3 + k4)

  def resolve(self, **kwargs):
    """
    Résoud le système d'EDO sur un certain range de temps.
    Soit l'intervalle complète, soit une sous-intervalle.
    @sub_interval : ndarray contenant contenant tous les temps de la sous-intervalle.
    """
    print("resolving...")

    # [
    #   f(0), f'(0), f''(0)], theta(0), theta'(0)
    # ]
    # where f''(0) is the shoot way of f'(n => infty)
    # where theta'(0) is the shoot way of theta(n => infty)
    y = np.array(self.ci)

    index_start = int(self.full_time_range[0] / self.time_step)

    self.y_set[0] = y.copy()

    # on ne calcule pas l'approximation
    # pour la première valeur de temps (t_initial)
    # car celle-ci correspond aux conditions initiales
    for index, t in enumerate(self.full_time_range[1:]):
      # resolve each first order edo (e.g. position (x'), speed (v'))
      y += (self.time_step / 6) * self.derivatives(y)

      self.y_set[index] = y.copy()
