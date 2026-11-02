## Weight Analysis model
# Model 33, Cruise Velocity

import numpy

def Cruise_Velocity(W_by_S, rho, Cdo, K_lift):

    Vc = numpy.sqrt((2*W_by_S)/(rho*numpy.sqrt(Cdo/K_lift)))

    return Vc
