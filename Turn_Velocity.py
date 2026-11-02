## Weight Analysis model
# Model 30, Turn Velocity

import numpy

def Turn_Velocity(rho, W_by_S, Cl_max):

    Vt = 1.2*numpy.sqrt((2*W_by_S)/(rho*Cl_max))

    return Vt
