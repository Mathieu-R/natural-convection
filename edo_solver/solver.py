import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from utils import seconds_to_hour

matplotlib.rcParams['toolbar'] = 'None'
matplotlib.rcParams['text.usetex'] = True

class EDONumericalResolution:
  def __init__(self, edo, ci, full_time_range, time_step):
    """
    @edo: fonction qui retourne [y' = CI, y'' = EDO] sous forme de matrice
    @ci : liste des conditions initiales
    @full_time_range : ndarray contenant [time_start -> time_end] pour chaque time_step
    @time_step : intervalle de temps
    """
    # edo => function that return [y' = CI, y'' = EDO] as a matrix
    # flow and heat edo are coupled
    # we use one array for the two coupled edo
    # [f, f', f'', theta, theta']
    self.edo = edo
    self.ci = ci
    self.full_time_range = full_time_range
    self.time_step = time_step

    self.prandtl = 0.01

    # keep track of data
    #self._time_set = np.zeros([len(full_time_range)])
    self.y_set = np.zeros([len(full_time_range), len(ci)])

  def resolve(self, **kwargs):
    raise NotImplemented

  # we plot f'(eta) and theta(eta)
  # remember: after integration => self.y_set [...,[f, f', f'', theta, theta'],...]
  def graph(self, title, edo_legends, x_label, y_label):
    plt.plot(self.full_time_range, self.y_set[:, 0], 'b')
    #plt.plot(self.full_time_range, self.y_set[:, 3], 'r')
    plt.title(title)
    # https://stackoverflow.com/questions/44632571/pyplot-legend-only-displaying-one-letter?noredirect=1&lq=1
    plt.legend(edo_legends, loc="upper right")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
