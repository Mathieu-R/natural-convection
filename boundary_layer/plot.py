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
    #ax.set_ylim(0, 2)
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


