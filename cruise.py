## Holistic model
# Model 37, Cruise

from Cruise_Velocity import Cruise_Velocity
from Cruise_Time import Cruise_Time
from Dynamic_Pressure import Dynamic_Pressure
from L_by_D_at_Cruise import L_by_D_at_Cruise
from Battery_Weight_Ratio_Cruise import Battery_Weight_Ratio_Cruise

# MATLAB globals, set by Main_Program before the mission runs
Cdo = np = nm = K_Battery = None

def cruise(rho, Xc, W_by_S, Vc, k_lift):

    # Vc = Cruise_Velocity(W_by_S, rho, Cdo, k_lift)
    Tc = Cruise_Time(Xc, Vc)
    q_c = Dynamic_Pressure(rho, Vc) # Dynamic Pressure for Cruise velocity
    L_by_D_c = L_by_D_at_Cruise(W_by_S, Cdo, q_c, k_lift)
    Wb_by_Wc = Battery_Weight_Ratio_Cruise(Xc, nm, np, L_by_D_c, K_Battery)

    return Wb_by_Wc
