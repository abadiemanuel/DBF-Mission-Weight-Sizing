## Holistic model
# Model 38, Loiter

from Loiter_Velocity import Loiter_Velocity
from Loiter_Distance import Loiter_Distance
from Dynamic_Pressure import Dynamic_Pressure
from L_by_D_at_Cruise import L_by_D_at_Cruise
from Battery_Weight_Ratio_Loiter import Battery_Weight_Ratio_Loiter

# MATLAB globals, set by Main_Program before the mission runs
np = nm = K_Battery = Cdo = None

def loiter(Vl, Tl, rho, W_by_S, k_lift):

    # Vl = Loiter_Velocity(W_by_S, rho, Cdo, K_lift)
    Ld = Loiter_Distance(Tl, Vl) # Loiter Distance in Km
    q_l = Dynamic_Pressure(rho, Vl) # Dynamic Pressure for Loiter velocity
    L_by_D_l = L_by_D_at_Cruise(W_by_S, Cdo, q_l, k_lift)
    Wb_by_Wl = Battery_Weight_Ratio_Loiter(Ld, nm, np, L_by_D_l, K_Battery)
    # Tl = Loiter_Time(Ld, Vl) # Loiter time in seconds

    return Wb_by_Wl
