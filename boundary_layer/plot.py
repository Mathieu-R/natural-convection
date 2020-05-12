import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['toolbar'] = 'None'
matplotlib.rcParams['text.usetex'] = True

class plot():
  @staticmethod
  def natural_convection(stream, plate, bl, delta_estimated):
    fig = plt.figure(1)

    ax = fig.add_subplot(211)
    ax.plot(plate.eta_range, bl.df, "b-", label="$f'(\eta)$")
    ax.plot(plate.eta_range, bl.theta, "r-", label="$\\theta(\eta)$")
    ax.set_title("Convection naturelle - solution de similitude")
    ax.set_xlabel("$\\eta$")
    ax.set_xlim(0, plate.eta_max)
    ax.set_ylim(0, 10)
    ax.legend(fontsize=11)

    plt.show()

    # ax = fig.add_subplot(212)
    # #ax.pcolor(plate.X, plate.Y, bl.u)
    # #ax.plot(plate.x, bl.delta,'b-', label="$\delta$")
    # #ax.plot(plate.x, bl.delta_star,'r-', label="$\delta^*$")
    # ax.set_title("Convection naturelle - couche limite")
    # ax.set_xlabel("$x(m)$")
    # ax.set_ylabel("$y(m)$")
    # ax.set_xlim(0, 8 * delta_estimated)
    # ax.set_ylim(0, 1)
    # ax.legend(fontsize=11)



# # we plot f'(eta) and theta(eta)
# # remember: after integration => self.y_set [...,[f, f', f'', theta, theta'],...]
# def plot(eta_range, y_set, title, edo_legends, x_label, y_label):
#   plt.plot(eta_range, y_set[:, 1], 'b')
#   plt.plot(eta_range, y_set[:, 3], 'r')
#   plt.title(title)
#   # https://stackoverflow.com/questions/44632571/pyplot-legend-only-displaying-one-letter?noredirect=1&lq=1
#   plt.legend(edo_legends, loc="upper right")
#   plt.xlabel(x_label)
#   plt.ylabel(y_label)
#   plt.show()

# def heatmap(eta_range, y_set, title, edo_legends, x_label, y_label):
#   # it should be distance x distance
#   # we should have the height of the plate
#   contour = plt.contour(eta_range, y_set[:, 3], 'r')
#   colorbar = plt.colorbar(contour)
#   colorbar.ax.set_ylabel("Température adimensionnelle")
#   plt.title(title)
#   plt.xlabel(x_label)
#   plt.ylabel(y_label)
#   plt.show()

