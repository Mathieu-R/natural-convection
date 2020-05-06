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
from scipy.optimize import newton

from decimal import Decimal
from edo_solver.edo import basic_blasius_edo, blasius_edo
from edo_solver.plot import plot

from constants import PRECISION

def rk4(eta_range, shoot):
  prandtl = 0.01

  # initial values
  f_init = [0, 0, shoot] # f(0), f'(0), f''(0)
  theta_init = [1, shoot] # theta(0), theta'(0)
  ci = f_init + theta_init # concatenate two ci

  # note: tuple with single argument must have "," at the end of the tuple
  return odeint(func=blasius_edo, y0=ci, t=eta_range, args=(prandtl,))

"""
if we have :
f'(t_0) = fprime_t0 ; f'(eta -> infty) = fprime_inf
we can transform it into :
f'(t_0) = fprime_t0 ; f''(t_0) = a

we define the function F(a) = f'(infty ; a) - fprime_inf
if F(a) has a root in "a",
then the solutions to the initial value problem with f''(t_0) = a
is also the solution the boundary problem with f'(eta -> infty) = fprime_inf

our goal is to find the root, we have the root...we have the solution.
it can be done with bissection method or newton method.
"""
def shooting(eta_range):
  # boundary value
  fprimeinf = 0 # f'(eta -> infty) = 0

  # initial guess
  # as far as I understand
  # it has to be the good guess
  # otherwise the result can be completely wrong
  initial_guess = 10 # guess for f''(0)

  # define our function to optimize
  # our goal is to take big eta because eta should approach infty
  # [-1, 2] : last row, second column => f'(eta_final) ~ f'(eta -> infty)
  fun = lambda initial_guess: rk4(eta_range, initial_guess)[-1, 1] - fprimeinf
  # newton method resolve the ODE system until eta_final
  # then adjust the shoot and resolve again until we have a correct shoot
  shoot = newton(func=fun, x0=initial_guess)

  # resolve our system of ODE with the good "a"
  y = rk4(eta_range, shoot)
  return y

def compute_blasius_edo(title, eta_final):
  ETA_0 = 0
  ETA_INTERVAL = 0.1
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
