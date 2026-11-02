## Aircraft model
# Model 5, Stall Velocity

import numpy

def Stall_Velocity(W_by_S, rho, Clmax):

    Vs = numpy.sqrt((2*W_by_S)/(rho*Clmax))

    return Vs
