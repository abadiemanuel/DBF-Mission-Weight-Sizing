## Weight Analysis model
# Model 26, Loiter velocity

import numpy

def Loiter_Velocity(W_by_S, rho, Cdo, K_lift):

    Vl = numpy.sqrt(((2*W_by_S)/rho)*(K_lift/(3*Cdo)))

    return Vl
