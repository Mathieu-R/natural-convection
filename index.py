"""
The goal is to resolve a 3rd order non-linear ODE for the blasius problem.
It's made of 2 equations (flow / heat)

f''' = 3ff'' - 2(f')^2 + theta
3 Pr f theta' + theta'' = 0

RK4 + Shooting Method

CHECK : testes with basic_blasius_edo and compared with Legat graph and it works.
"""

import numpy as np

from scipy.integrate import odeint
from scipy.optimize import newton, brentq

from decimal import Decimal
from edo_solver.edo import basic_blasius_edo, blasius_edo
from edo_solver.plot import plot

from constants import PRECISION

def rk4(eta_range, shoot_f, shoot_theta):
  prandtl = 0.01

  # initial values
  f_init = [0, 0, shoot_f] # f(0), f'(0), f''(0)
  theta_init = [1, shoot_theta] # theta(0), theta'(0)
  ci = f_init + theta_init # concatenate two ci

  # note: tuple with single argument must have "," at the end of the tuple
  return odeint(func=blasius_edo, y0=ci, t=eta_range, args=(prandtl,), tfirst=True)

def compute_blasius_edo(title, eta_final):
  ETA_0 = 0
  ETA_INTERVAL = 0.01
  ETA_FINAL = eta_final

  # default values
  title = title
  x_label = "$\eta$"
  y_label = "profil de vitesse $(f'(\eta))$ / profil de température $(\\theta)$"
  legends = ["$f'(\eta)$", "$\\theta$"]

  eta_range = np.arange(ETA_0, ETA_FINAL + ETA_INTERVAL, ETA_INTERVAL)

  # shoot
  y_set = shooting(eta_range)

  plot(eta_range, y_set, title, legends, x_label, y_label)

compute_blasius_edo(
  title="Convection naturelle - Solution de similitude",
  eta_final=10
)
