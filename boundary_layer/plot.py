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
    ax.plot(plate.x_mesh, bl.result.sol(plate.x_mesh)[1], "b-", label="$f'(\eta)$")
    ax.plot(plate.x_mesh, bl.result.sol(plate.x_mesh)[3], "r-", label="$\\theta(\eta)$")
    ax.set_title("Convection naturelle - solution de similitude")
    ax.set_xlabel("$\\eta$")
    ax.set_xlim(0, plate.eta_max)
    #ax.set_ylim(0, 2)
    ax.legend(fontsize=11)

    plt.show()

