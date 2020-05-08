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
from scipy.optimize import bisect

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

NOTE :  we have two boundary values for the 2 coupled ODE.
        I guess we should manage these two in parallel.
"""
def shooting(eta_range):
  # boundary values
  #fprimeinf = 0 # f'(eta -> infty) = 0
  #thetainf = 0 # theta(eta -> infty) = 0

  # initial guess
  # as far as I understand
  # it has to be the good guess
  # otherwise the result can be completely wrong
  #f_initial_guess = 10 # guess for f''(0)
  #theta_initial_guess = 100 # guess for theta'(0)

  # define our function to optimize
  # our goal is to take big eta because eta should approach infty
  # [-1, 1] : last row, second column => f'(eta_final) ~ f'(eta -> infty)
  # [-1, 3] : last row, fourth column => theta(eta_final) ~ theta(eta -> infty)
  #fun_f = lambda initial_guess: rk4(eta_range, f_initial_guess, theta_initial_guess)[-1, 1] - fprimeinf
  #fun_theta = lambda initial_guess: rk4(eta_range, f_initial_guess, initial_guess)[-1, 3] - thetainf
  # newton method resolve the ODE system until eta_final
  # then adjust the shoot and resolve again until we have a correct shoot
  #shoot_f = newton(func=fun_f, x0=f_initial_guess)
  #shoot_theta = newton(func=fun_theta, x0=theta_initial_guess)
  #shoot_f = bisect(f=fun_f, a=0, b=10)
  #shoot_theta = bisect(f=fun_theta, a=0, b=10)

  #print(shoot_f, shoot_theta)

  shoot_flow, shoot_heat = bisection(eta_range)

  print(shoot_flow, shoot_heat)

  # resolve our system of ODE with the good "a"
  y = rk4(eta_range, shoot_flow, shoot_heat)
  return y

# https://www.math.ubc.ca/~pwalls/math-python/roots-optimization/bisection/
def bisection(eta_range):
  # we choose a starting interval [a0, b0]
  # such that f(a0)*f(b0) < 0
  a0_flow = 0
  b0_flow = 1

  a0_heat = 0
  b0_heat = 1

  f_a0 = rk4(eta_range, a0_flow, a0_heat)
  f_b0 = rk4(eta_range, b0_flow, b0_heat)

  f_a0_flow = f_a0[-1, 1]
  f_b0_flow = f_b0[-1, 1]

  f_a0_heat = f_a0[-1, 3]
  f_b0_heat = f_b0[-1, 3]

  # Intermediate value problem
  # function has a root if it changes of sign over the interval
  if (f_a0_flow * f_b0_flow) >= 0:
    print("Wrong interval for flow")
    return

  if (f_a0_heat * f_b0_heat) >= 0:
    print("Wrong interval for heat")
    return

  # we decide to loop 40 times
  for i in range(1,40):
    # compute middle point
    midpoint_flow = (a0_flow + b0_flow) / 2
    midpoint_heat = (a0_heat + b0_heat) / 2

    f_midpoint = rk4(eta_range, midpoint_flow, midpoint_heat)

    f_midpoint_flow = f_midpoint[-1, 1]
    f_midpoint_heat = f_midpoint[-1, 3]

    # determine the next subinterval
    if (f_a0_flow * f_midpoint_flow) < 0:
      b0_flow = midpoint_flow

    elif (f_b0_flow * f_midpoint_flow) < 0:
      a0_flow = midpoint_flow

    if (f_a0_heat * f_midpoint_heat) < 0:
      b0_heat = midpoint_heat

    elif (f_b0_heat * f_midpoint_heat) < 0:
      a0_heat = midpoint_heat

    # check precision
    if abs(midpoint_flow) <= PRECISION and abs(midpoint_heat) <= PRECISION:
      print("got precision")
      break

  # should be a good approximation of the root
  return midpoint_flow, midpoint_heat

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
