## Holistic model
# Model 36 Take-off

from Stall_Velocity import Stall_Velocity
from Takeoff_Velocity import Takeoff_Velocity
from Takeoff_Distance import Takeoff_Distance
from Takeoff_Time import Takeoff_Time
from Battery_Weight_Ratio_Takeoff import Battery_Weight_Ratio_Takeoff

# MATLAB globals, set by Main_Program before the mission runs
g = np = nm = K_Battery = Cl_max = None

def takeoff(rho, W_by_S, P_to_W):

    Vs = Stall_Velocity(W_by_S, rho, Cl_max) # Stall Velocity
    Vto = Takeoff_Velocity(Vs) # Takeoff Velocity
    Xto = Takeoff_Distance(Vto, g, nm, np, P_to_W) # Takeoff Distance
    Tto = Takeoff_Time(Vto, g, nm, np, P_to_W)
    Wb_by_Wto = Battery_Weight_Ratio_Takeoff(Tto, P_to_W, K_Battery)

    return Wb_by_Wto
