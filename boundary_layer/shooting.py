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
    self, ode, initial_values, boundary_values,
    t_range, guesses, args = (),
    iterations = 200, precision = 1e-7
  ):

    self.iterations = 200
    self.precision = 1e-7
    self.guesses = guesses
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
    errors = []
    for guess in self.guesses:
      error = f[-1][guess["boundary_position"]] - self.boundary_values[guess["boundary_position"]]
      errors.append(error)

    return errors

  def plot_error_function(self):
    boundary_errors = []
    for guess in np.linspace(0, 5):
      for guess in self.guesses:
        # put the guess
        self.initial_values[guess["guess_position"]] = guess["guesses"][1]

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


  def do_we_get_closer_to_boundary_condition(self, boundary_error_0, boundary_error_1, guess_0, guess_1):
    print(f"convergence: {abs(boundary_error_1 - boundary_error_0)}")
    if (abs(boundary_error_1 - boundary_error_0) > 0.0):
      return -boundary_error_1 * ((guess_1 - guess_0) / float(boundary_error_1 - boundary_error_0))
    else:
      return 0.0

  def first_guess(self):
    for guess in self.guesses:
      # try with the first guess for the unknown initial value
      self.initial_values[guess["guess_position"]] = guess["guesses"][0]

      # resolve ode
    f = odeint(func=self.df, y0=self.initial_values, t=self.t_range, args=self.args, tfirst=True)

    # compute boundary error
    boundary_errors = self.boundary_error(f)
    return boundary_errors

  def shoot(self):
    boundary_errors_0 = self.first_guess()

    # loop until we get the solutions
    # that satisfies the boundary condition
    for i in range(self.iterations):
      # updating initial value with the next guess

      for guess in self.guesses:
        self.initial_values[guess["guess_position"]] = guess["guesses"][1]

      print(self.initial_values)

      # resolve ode
      f = odeint(func=self.df, y0=self.initial_values, t=self.t_range, args=self.args, tfirst=True)

      # compute boundary error
      boundary_errors_1 = self.boundary_error(f)

      delta_boundary_array = []

      # for each boundary value (1 array of guess = 1 boundary value)
      for index, guess in enumerate(self.guesses):
        # check if we get closer to the boundary condition
        delta_boundary = self.do_we_get_closer_to_boundary_condition(
          boundary_errors_0[index], boundary_errors_1[index],
          guess["guesses"][0], guess["guesses"][1]
        )
        print(delta_boundary)
        delta_boundary_array.append(delta_boundary)

        # updating guesses
        guess["guesses"][0] = guess["guesses"][1]
        guess["guesses"][1] += delta_boundary
        boundary_errors_0[index] = boundary_errors_1[index]

      # convergence criteria
      if all(abs(delta_boundary) <= self.precision for delta_boundary in delta_boundary_array):
        print("convergence criteria satisfied for each boundary value.")
        break

    return f

