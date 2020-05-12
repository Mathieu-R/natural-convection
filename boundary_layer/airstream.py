class airstream():
  def __init__(self, airspeed, length):
    self.ue = airspeed # air stream velocity
    self.P = 101325 # Atmospheric pressure
    self.Te = 300 # Air temperature (K)
    self.lambd = 0.02 # Air thermal conductivity
    self.cp = 0.3 # Air specific heat

    self.L = length # Characteristic length (here we're gonna choose the same length as plate length)

    # Dynamic viscosity
    # Approximated with Sutherland viscosity law
    # For air at moderate temperature and pressure
    # http://jullio.pe.kr/fluent6.1/help/html/ug/node294.htm
    self.mu = (1.458*10e-6 * (self.Te ** (3/2))) / (self.Te + 110.4)

    # rho for ideall gas in meteorology
    # cp - cv ~ 287
    # https://fr.wikipedia.org/wiki/Loi_des_gaz_parfaits#%C3%89nonc%C3%A9_en_m%C3%A9t%C3%A9orologie
    self.rho = self.P / (287 * self.Te)

    # Kinematic viscosity
    self.nu = self.mu / self.rho

    # Air Reynold Number
    # inertia force / viscous force
    # predict flow pattern (laminar, turbulent)
    self.Re = (self.ue * self.L) / self.nu

    # Air thermic diffusivity
    # capacity of a material to send a signal of temperature
    # from a specific point to another
    self.alpha = self.lambd / (self.rho * self.cp)

    # Air Prandtl Number
    # diffusivity of momentum / diffusivity of heat
    # Big Prandtl => temperature profil highly influenced by velocity profile
    # Little Prandtl => high speed thermal conductivity => not much influcence
    self.Prandtl = self.nu / self.alpha
