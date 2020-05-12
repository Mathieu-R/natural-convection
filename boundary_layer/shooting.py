import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from scipy.integrate import odeint

"""
shooting method to resolve boundary value problem.
ode : ordinary differential equation system to resolve.
initial_values: array of initial values [f(0), f'(0),...]
boundary_values: array of boundary values [f(infty), f'(infty)]
guesses: array of guesses for the unknwon initial value.
guess_position: position of the guess in the initial_values array.
boundary_position: position of the boundary_value to compare.
args = (): tuple of supplementary args to pass to scipty odeint (default: ()).
iterations: max numbers of iterations for the shooting algorithm (default: 200).
precision: precision of the initial value (default: 1e-7).
"""
class shooting():
  def __init__(
    self, ode, initial_values, boundary_values, t_range,
    guesses, guess_position, boundary_position,
    args = (), iterations = 200, precision = 1e-7
  ):
    super().__init__()

    # [-1, -10e-5, 10e-5, 1]
    self.iterations = 200
    self.precision = 1e-7
    self.guesses = guesses
    self.guess_position = guess_position
    self.boundary_position = boundary_position
    self.t_range = t_range

    self.initial_values = initial_values
    self.boundary_values = boundary_values
    self.df = ode

    self.args = args

  """
  compare the computed value at the end of the interval
  with the boundary value given
  => should be equal to zero
  e.g. f'(eta = "big_number") - f'(eta -> infty)
  """
  def boundary_error(self, f):
    error = f[-1][self.boundary_position] - self.boundary_values[self.boundary_position]
    return error

  def plot_error_function(self):
    boundary_errors = []
    for guess in np.linspace(0, 5):
      # put the guess
      self.initial_values[self.guess_position] = guess

      # resolve edo
      f = odeint(func=self.df, y0=self.initial_values, t=self.t_range, args=self.args, tfirst=True)

      boundary_errors.append(boundary_error(f))

    fig = plt.figure(1)
    plt.plot(self.guesses, boundary_errors)
    plt.title('Boundary errors')
    plt.ylabel('boundary errors')
    plt.xlabel('guesses')
    # plt.xlim(0,5)
    # plt.ylim(-1,4)
    # plt.grid(b=True, which='both')

  def do_we_get_closer_to_boundary_condition(self, boundary_error_0, boundary_error_1):
    print(boundary_error_1, boundary_error_0)
    if (abs(boundary_error_1 - boundary_error_0) > 0.0):
      return -boundary_error_1 * ((self.guesses[1] - self.guesses[0]) / float(boundary_error_1 - boundary_error_0))
    else:
      return 0.0

  def first_guess(self):
    # try with the first guess for the unknown initial value
    self.initial_values[self.guess_position] = self.guesses[0]

    # resolve ode
    f = odeint(func=self.df, y0=self.initial_values, t=self.t_range, args=self.args, tfirst=True)

    # compute boundary error
    boundary_error = self.boundary_error(f)
    return boundary_error

  def shoot(self):
    boundary_error_0 = self.first_guess()

    # loop until we get the solutions
    # that satisfies the boundary condition
    for i in range(self.iterations):
      # resolve ode
      f = odeint(func=self.df, y0=self.initial_values, t=self.t_range, args=self.args, tfirst=True)

      # compute boundary error
      boundary_error_1 = self.boundary_error(f)

      # check if we get closer to the boundary condition
      delta_boundary = self.do_we_get_closer_to_boundary_condition(boundary_error_0, boundary_error_1)

      # updating guesses
      self.guesses[0] = self.guesses[1]
      self.guesses[1] += delta_boundary
      boundary_error_0 = boundary_error_1

      # convergence criteria
      if (abs(delta_boundary) <= self.precision):
        break

    return f

