## Weight Analysis model
# Model 31, Load Factor for Turns

import numpy

def Load_factor(q_t, k_lift, W_by_S, P_to_W, nm, np, Vt, Cdo):

    # emath.sqrt returns a complex number for a negative argument, like MATLAB's sqrt
    n = numpy.emath.sqrt((q_t/(k_lift*W_by_S)*(P_to_W*nm*np/Vt-q_t*Cdo/W_by_S)))

    return n
