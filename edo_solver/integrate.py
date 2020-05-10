import numpy as np

def derivatives_rk4(fun, t, y, time_step):
    k1 = fun(t, y)
    k2 = fun(t + (time_step / 2), y + ((time_step / 2) * k1))
    k3 = fun(t + (time_step / 2), y + ((time_step / 2) * k2))
    k4 = fun(t + time_step, y + (time_step * k3))
    return (k1 + 2*k2 + 2*k3 + k4)


def solve_rk4(func, y0, t, args=()):
  # wrap function with args
  fun = lambda t, x, fun=func: fun(t, x, *args)
  # evenly spaced time-step
  time_step = t[1] - t[0]
  print(time_step)

  results = np.zeros((len(t), len(y0)))
  results[0] = np.array(y0)
  y = np.array(y0)

  for time in t:
    # 0, 1, 2, 3, ...
    index = int(time / time_step)
    y += (time_step / 6) * derivatives_rk4(fun, time, y, time_step)

    results[index] = y.copy()

  return results



