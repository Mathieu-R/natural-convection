import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['toolbar'] = 'None'
matplotlib.rcParams['text.usetex'] = True

# we plot f'(eta) and theta(eta)
# remember: after integration => self.y_set [...,[f, f', f'', theta, theta'],...]
def plot(eta_range, y_set, title, edo_legends, x_label, y_label):
  plt.plot(eta_range, y_set[:, 0], 'b')
  plt.plot(eta_range, y_set[:, 3], 'r')
  plt.title(title)
  # https://stackoverflow.com/questions/44632571/pyplot-legend-only-displaying-one-letter?noredirect=1&lq=1
  plt.legend(edo_legends, loc="upper right")
  plt.xlabel(x_label)
  plt.ylabel(y_label)
  plt.show()

