from boundary_layer.airstream import airstream
from boundary_layer.flat_plate import plate
from boundary_layer.boundary_layer import boundary_layer
from boundary_layer.plot import plot

L = 1 # characteristic length / plate length
ue = 10 # airspeed

# fluid
stream = airstream(airspeed=ue, length=L)

# estimation of the boundary tickness
delta_estimated = L / (stream.Re**0.5)

# flat hot plate
hot_plate = plate(length=L, t_wall=300, eta_max=10)
hot_plate.mesh(delta_estimated=delta_estimated, ue=ue, nu=stream.nu)

# boundary layer
bl = boundary_layer(stream=stream, plate=hot_plate, Pr=0.01)

# plot
plot.natural_convection(stream=stream, plate=hot_plate, bl=bl, delta_estimated=delta_estimated)
