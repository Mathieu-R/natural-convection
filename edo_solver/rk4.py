import numpy as np
import matplotlib.pyplot as plt

from .solver import EDONumericalResolution
from utils import seconds_to_hour

class RK4Method(EDONumericalResolution):
  def derivatives(self, tn, y):
    k1 = self.edo(self, tn, y)
    k2 = self.edo(self, tn + (self.time_step / 2), y + ((self.time_step / 2) * k1))
    k3 = self.edo(self, tn + (self.time_step / 2), y + ((self.time_step / 2) * k2))
    k4 = self.edo(self, tn + self.time_step, y + (self.time_step * k3))
    return (k1 + 2*k2 + 2*k3 + k4)

  def resolve(self, **kwargs):
    """
    Résoud le système d'EDO sur un certain range de temps.
    Soit l'intervalle complète, soit une sous-intervalle.
    @sub_interval : ndarray contenant contenant tous les temps de la sous-intervalle.
    """
    print("resolving...")

    if ("sub_interval" in kwargs):
      time_range = kwargs.get("sub_interval")
    else:
      time_range = self.full_time_range

    y = np.array(self.ci) # [I(0), X(0), PHI(0)]

    # exemple : start: 3600s = 1h, time_step = 10s => index_start = 360
    # exemple : end: 7190s = 1h59m50s, time_step = 10s => index_end = 719
    index_start = int(time_range[0] / self.time_step)
    # index_end = sub_interval[-1] / self.time_step

    self.y_set[index_start] = y.copy()

    # on ne calcule pas l'approximation
    # pour la première valeur de temps (t_initial)
    # car celle-ci correspond aux conditions initiales
    for t in time_range[1:]:
      # 0, 1, 2, 3, ...
      index = int(t / self.time_step)
      # resolve each first order edo (e.g. position (x'), speed (v'))
      y += (self.time_step / 6) * self.derivatives(t, y)

      #self.time_set.append(seconds_to_hour(t))
      self.y_set[index] = y.copy()