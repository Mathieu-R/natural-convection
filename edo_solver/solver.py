import matplotlib.pyplot as plt
import numpy as np

from utils import seconds_to_hour

class EDONumericalResolution:
  def __init__(self, edo, flow_ci, heat_ci, full_time_range, time_step):
    """
    @edo: fonction qui retourne [y' = CI, y'' = EDO] sous forme de matrice
    @ci : liste des conditions initiales
    @full_time_range : ndarray contenant [time_start -> time_end] pour chaque time_step
    @time_step : intervalle de temps
    """
    # array of edo => functions that return [y' = CI, y'' = EDO] as a matrix
    self.edo = edo
    self.flow_ci = flow_ci
    self.heat_ci = heat_ci
    self.full_time_range = full_time_range
    self.time_step = time_step
    
    self.prandtl = 0.01

    # keep track of data
    #self._time_set = np.zeros([len(full_time_range)])
    self.flow_y_set = np.zeros([len(full_time_range), len(flow_ci)])
    self.heat_y_set = np.zeros([len(full_time_range), len(heat_ci)])

  def resolve(self, **kwargs):
    raise NotImplemented

  def graph(self, title, edo_legends, x_label, y_label):
    full_time_range_in_hours = np.fromiter(map(lambda t: seconds_to_hour(t), self.full_time_range), dtype=np.float)
    plt.plot(full_time_range_in_hours, self.y_set)
    plt.title(title)
    # https://stackoverflow.com/questions/44632571/pyplot-legend-only-displaying-one-letter?noredirect=1&lq=1
    plt.legend(edo_legends, loc="upper right")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.yscale('log')
    plt.show()