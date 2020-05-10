from constants import PRECISION

"""
  root finding algorithm using secant method
  fun: function to optimize
  a0, b0: starting interval
  iterations: number of iterations
"""
def secant(fun, a0, b0, iterations=100):
  delta = 0.05

  a = a0
  b = b0

  fa = fun(a)
  fb = fun(b)

  fafb = fa * fb

  # fafb should be negative to ensure a root exists
  # we fix a maximal interval length
  while (fafb >= 0) and (abs(b - a) <= 200):
    #print(fb)
    #print("fafb >= 0, looking for root...")
    # increase interval of a step delta
    b += delta
    fa = fun(a)
    fb = fun(b)
    fafb = fa*fb

  # if we couldn't find an interval s.t fa*fb < 0
  # stop here...
  if (fafb >= 0):
    print(f"This function has no root on the interval (overevaluated) [{a}, {b}]...")

  print("root exist")

  for i in range(1,iterations):
    # compute secant line
    x = a - (fa * ((b - a) / (fb - fa)))
    fx = fun(x)

    # determine the next interval
    if (fa * fx) < 0:
      a = a
      b = x

      # reevaluate f(b)
      fb = fun(b)

    elif (fb * fx) < 0:
      a = x
      b = b

      # reevaluate f(a)
      fa = fun(a)

    elif fx == 0:
      print("Exact solution found.")
      return x

    # stop when our interval has reached some
    # predetermined length
    if (abs(a - b) <= PRECISION):
      return x

  return x
