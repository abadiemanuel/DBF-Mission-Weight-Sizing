## Weight Analysis model
# Model 32, Battery Weight ratio for Turns

import math
import numpy

def Battery_Weight_Ratio_Turn(P_to_W, Vt, K_Battery, g, n, theta):

    Wb_by_Wt = (2*math.pi*P_to_W*Vt*theta)/(K_Battery*g*numpy.emath.sqrt((n)**2-1))

    return Wb_by_Wt
