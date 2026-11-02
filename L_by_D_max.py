## Aircraft model
# Model 4, Maximum Lift to drag ratio

import math

def L_by_D_max(e, AR, Cdo):

    L_by_D_max = 0.5*(((math.pi * e * AR)/ Cdo)**(0.5))

    return L_by_D_max
