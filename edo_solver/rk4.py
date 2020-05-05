import numpy as np
import matplotlib.pyplot as plt

from .solver import EDONumericalResolution
from utils import seconds_to_hour

class RK4Method(EDONumericalResolution):
  def derivatives(self, tn, flow_y, heat_y):
    computations = []
    for edo in self.edo:
      k1 = edo(self, tn, flow_y, heat_y)
      print("oh shiiiit")
      print(k1)
      print(flow_y)
      print(heat_y)
      print(self.time_step)
      k2 = edo(self, tn + (self.time_step / 2), flow_y + ((self.time_step / 2) * k1), heat_y + ((self.time_step / 2) * k1))
      k3 = edo(self, tn + (self.time_step / 2), flow_y + ((self.time_step / 2) * k2), heat_y + ((self.time_step / 2) * k2))
      k4 = edo(self, tn + self.time_step, flow_y + (self.time_step * k3), heat_y + (self.time_step * k3))
      computations.append(k1 + 2*k2 + 2*k3 + k4)
    return computations[0], computations[1]

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

    # [
    #   [f(0), f'(0), f''(0)],
    #   [theta(0), theta'(0)]
    # ]
    # where f''(0) is the shoot way of f'(n => infty)
    # where theta'(0) is the shoot way of theta(n => infty)
    flow_y = np.array(self.flow_ci) 
    heat_y = np.array(self.heat_ci)

    # exemple : start: 3600s = 1h, time_step = 10s => index_start = 360
    # exemple : end: 7190s = 1h59m50s, time_step = 10s => index_end = 719
    index_start = int(time_range[0] / self.time_step)
    # index_end = sub_interval[-1] / self.time_step

    print(self.flow_y_set[index_start])
    print(flow_y)
    self.flow_y_set[index_start] = flow_y.copy()
    self.heat_y_set[index_start] = heat_y.copy()

    # on ne calcule pas l'approximation
    # pour la première valeur de temps (t_initial)
    # car celle-ci correspond aux conditions initiales
    for t in time_range[1:]:
      # 0, 1, 2, 3, ...
      index = int(t / self.time_step)
      # resolve each first order edo (e.g. position (x'), speed (v'))
      new_flow_y, new_heat_y = self.derivatives(t, flow_y, heat_y)
      flow_y += (self.time_step / 6) * new_flow_y
      heat_y += (self.time_step / 6) * new_heat_y

      #self.time_set.append(seconds_to_hour(t))
      self.flow_y_set[index] = flow_y.copy()
      self.heat_y_set[index] = heat_y.copy()