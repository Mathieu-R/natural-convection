"""
The goal is to resolve a 3rd order non-linear ODE for the blasius problem.
It's made of 2 equations (flow / heat)

f''' = 3ff'' - 2(f')^2 + theta
3 Pr f theta' + theta'' = 0

RK4 + Shooting Method
"""

import numpy as np

from decimal import Decimal
from edo_solver.rk4 import RK4Method
from edo_solver.edo import basic_blasius_edo, blasius_edo

from utils import day_to_seconds, hour_to_seconds, minute_to_seconds, seconds_to_hour
from constants import PRECISION

def compute_blasius_edo(title, stop):
  # default values
  T0 = 0
  ETA_INTERVAL = 0.1
  STOP = stop

  title = title
  x_label = "$\eta$"
  y_label = ""
  legends = ["$f'(\eta)$", "$\\theta$"]

  # time range which is not a time range in this case
  # I think the absciss is eta
  full_time_range = np.arange(T0, STOP + ETA_INTERVAL, ETA_INTERVAL)

  # boundary value
  fprimeinf = 0 # f'(eta -> infty) = 0
  fprimeguess = 1 # guess for f''(0)

  # starting value for missing conditions
  # f''(0) = a
  s_1 = 0.0
  s_2 = 1.0

  print(s_1, s_2)

  n = 1
  iter_max = 40

  # SHOOT
  while (abs(fprimeguess - fprimeinf) > PRECISION and n <= iter_max):
    # because f'(b) = 0 (btw, "b" is our way to do eta -> infty ; we take "b" big enough)
    # so we choose f''(0) = s_1 and f''(0) = s_2
    # such that f'(b) = r_1 and f'(b) = r_2
    # and r_1 <= 0 <= r_2

    # then we solve the EDO for f''(0) = s
    s = ((s_1 + s_2) / 2)

    # initial values
    f_init = [0, 0, s] # f(0), f'(0), f''(0)
    theta_init = [1, s] # theta(0), theta'(0)
    ci = f_init + theta_init # concatenate two ci

    flow = RK4Method(blasius_edo, ci, full_time_range, ETA_INTERVAL)
    flow.resolve()

    time = flow.full_time_range
    y_set = flow.y_set

    # then we choose the next s_1 and s_2
    # adjust our shoot
    # compare f'(eta)
    # y_set[-1, 1] := last row (last values calculated), 2nd column (f')
    fprimeguess = y_set[-1, 1]

    # if our guess is below the curve
    # we try to go upward
    # remember: s_1 <= s <= s_2
    if fprimeguess < fprimeinf:
      s_1 = s
    # if our guess is above the curve
    # we try to go downward
    else:
      s_2 = s

    n += 1

  flow.graph(title, legends, x_label, y_label)

compute_blasius_edo(
  title="Convection naturelle - Solution de similitude",
  stop=4
)
