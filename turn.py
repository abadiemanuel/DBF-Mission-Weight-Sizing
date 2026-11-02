## Holistic model
# Model 39, Turn

from Turn_Velocity import Turn_Velocity
from Dynamic_Pressure import Dynamic_Pressure
from Load_factor import Load_factor
from Battery_Weight_Ratio_Turn import Battery_Weight_Ratio_Turn

# MATLAB globals, set by Main_Program before the mission runs
g = Cdo = np = nm = K_Battery = Cl_max = None

def turn(rho, W_by_S, P_to_W, theta, k_lift):

    Vt = Turn_Velocity(rho, W_by_S, Cl_max)
    q_t = Dynamic_Pressure(rho, Vt) # Dynamic Pressure for Turn velocity
    n = Load_factor(q_t, k_lift, W_by_S, P_to_W, nm, np, Vt, Cdo)
    Wb_by_Wt = Battery_Weight_Ratio_Turn(P_to_W, Vt, K_Battery, g, n, theta)

    return Wb_by_Wt
