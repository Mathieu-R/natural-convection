"""
The goal is to resolve a 3rd order non-linear ODE for the blasius problem.
It's made of 2 equations (flow / heat)

f''' = 3ff'' - 2(f')^2 + theta = 0
3 Pr f theta' + theta'' = 0

RK4 + Shooting Method
"""

import numpy as np

from decimal import Decimal
from edo_solver.rk4 import RK4Method
from edo_solver.edo import blasius_edo_flow, blasius_edo_heat, blasius_edo

from utils import day_to_seconds, hour_to_seconds, minute_to_seconds, seconds_to_hour
from constants import PRECISION

def compute_blasius_edo(title, stop):
  # default values
  T0 = 0
  TIME_INTERVAL = 10 # 10s
  STOP = stop

  title = title
  x_label = ""
  y_label = ""
  legends = ['', '']

  full_time_range = np.arange(T0, STOP + TIME_INTERVAL, TIME_INTERVAL)

  # boundary value
  fprimeinf = 0 
  fprimeguess = 2

  # starting value for missing conditions
  # f''(0) = a
  s_1 = 0.1
  s_2 = 0.7

  while abs(fprimeguess - fprimeinf) > PRECISION:
    # because f'(b) = 0 (btw, "b" is our way to do eta -> infty ; we take "b" big enough)
    # so we choose f''(0) = s_1 and f''(0) = s_2 
    # such that f'(b) = r_1 and f'(b) = r_2
    # and r_1 <= 0 <= r_2

    # then we solve the EDO for f''(0) = s
    s = (s_1 + s_2) / 2

    # initial values
    f_init = [0, 0, s] # f(0), f'(0), f''(0)
    theta_init = [1, s] # theta(0), theta'(0)
    ci = [f_init, theta_init]

    fluid_flow = RK4Method(blasius_edo, ci, full_time_range, TIME_INTERVAL)
    fluid_flow.resolve()

    time = fluid_flow.full_time_range
    y_set = fluid_flow.y_set

    # then we choose the next s_1 and s_2
    # adjust our shoot
    print(y_set)
    if y_set[-1] < ...:
      s_1 = s
    else: 
      s_2 = s

    fprimeguess = y_set[-1]

    #fluid_flow.graph(title, legends, x_label, y_label)

compute_blasius_edo(
  title="",
  stop=minute_to_seconds(10)
)