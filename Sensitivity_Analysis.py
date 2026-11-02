# The MATLAB code modified to produce the table for sensitivity analysis

### Main Program

import math
import numpy

from density import density
from Stall_Velocity import Stall_Velocity
from Takeoff_Velocity import Takeoff_Velocity
from Dynamic_Pressure import Dynamic_Pressure

# Initial Values

rho_to = density(0) # Altitude in Feet

g = 9.8 # Acceleration due to gravity

# Airplane Models

AR = 8 # Aspect Ratio

Cdo_l = 0.02 #Drag Coefficient lower end
Cdo_u = 0.05 #Drag Coefficient upper end
e_l = 0.7 #Span Efficiency/ Oswald Efficiency lower end
e_u = 0.9 #Span Efficiency/ Oswald Efficiency upper end
np_l = 0.5 # Propeller Efficiency lower end
np_u = 0.85 # Propeller Efficiency upper end
nm_l = 0.65 # Motor Efficiency lower end
nm_u = 0.9 # Motor Efficiency upper end

Cl_min = 0.8 # min Lift Coefficient
Cl_max = 1.4 # Max Lift Coefficient

s = 1.73 # Wing Area m^2 OUTPUT
b = 3.72 # wing span m OUTPUT
Payload_wt = 10 # Payload weight in lbs
K_Battery = 48317.6204 # Battery Efficiency


Vthrow = 6 # Wind velocity or throw velocity in m/s
Xto = 1 # Takeoff Distance in m


# Variable that can be changed
We_to_WTo = 0.5 # Empty Weight to Take-Off Weight ratio

# Take Off

W_by_S_1 = numpy.arange(35, 81, 1.0)
N = len(W_by_S_1)

Vstall = numpy.zeros(N)
Vto = numpy.zeros(N)
P_to_W_T = numpy.zeros(N)

P_to_W_T_table = numpy.zeros((N, 8))

y = 0 # table column (MATLAB: for y = 1:1)
for k in [np_l, np_u]: # propeller Eff
    for j in [nm_l, nm_u]:
        for i in [Cl_min, Cl_max]:
            for h in range(N):

                Vstall[h] = Stall_Velocity(W_by_S_1[h], rho_to, i)

                Vto[h] = Takeoff_Velocity(Vstall[h])-Vthrow

                P_to_W_T[h] = (Vto[h]**3)/(2*g*j*k*Xto)

                P_to_W_T_table[h, y] = P_to_W_T[h]

            y = y+1


# Max Speed

rho_ms = density(150)

V_ms = 23 # Max Speed Velocity in m/s

q_ms = Dynamic_Pressure(rho_ms, V_ms) # Dynamic Pressure

k_lift = numpy.zeros(N)
L_by_D = numpy.zeros(N)
T_by_W_ms = numpy.zeros(N)
P_to_W_ms = numpy.zeros(N)

P_to_W_Ms_table = numpy.zeros((N, 16))

y = 0
for k in [np_l, np_u]:
    for j in [nm_l, nm_u]:
        for i in [Cdo_l, Cdo_u]:
            for l in [e_l, e_u]:
                for h in range(N):

                    k_lift[h] = 1/(math.pi * l * AR) # Drag Due to Lift min

                    L_by_D[h] = 1 /(2*math.sqrt(k_lift[h]*i)) # Min lift to drag ratio

                    T_by_W_ms[h] = (((q_ms*i/(W_by_S_1[h])) + ((k_lift[h] * W_by_S_1[h])/q_ms)))

                    P_to_W_ms[h] = (V_ms*T_by_W_ms[h])/(j*k)

                    P_to_W_Ms_table[h, y] = P_to_W_ms[h]

                y = y+1


# Approach Velocity

rho_app = density(100)

Vapp = 9 # Approach velocity in m/s

W_by_S_App_min = Dynamic_Pressure(rho_app, Vapp)*(Cl_min)*numpy.ones(10)
W_by_S_App_max = Dynamic_Pressure(rho_app, Vapp)*(Cl_max)*numpy.ones(10)

P_to_W_App = numpy.arange(0, 11, 1.0)


# Ceiling

rho_ceil = density(1900)

Cl_ceil = numpy.zeros(N)
Vceil = numpy.zeros(N)
P_to_W_Ceil = numpy.zeros(N)

P_to_W_Ceil_table = numpy.zeros((N, 16))

y = 0
for k in [np_l, np_u]:
    for j in [nm_l, nm_u]:
        for i in [Cdo_l, Cdo_u]:
            for l in [e_l, e_u]:
                for h in range(N):

                    k_lift[h] = 1/(math.pi * l * AR) # Drag Due to Lift min

                    Cl_ceil[h] = math.sqrt((3*i)/k_lift[h])

                    Vceil[h] = math.sqrt((2*W_by_S_1[h])/(rho_ceil*Cl_ceil[h]))

                    P_to_W_Ceil[h] = (Vceil[h]/(0.886*k*j*g))

                    P_to_W_Ceil_table[h, y] = P_to_W_Ceil[h]

                y = y+1


# Rate of Climb

rho_roc = 1.225
thrust = 1
ROC = 100 # Rate of climb in m/min

Cl_roc = numpy.zeros(N)
Vroc = numpy.zeros(N)
P_to_W_roc = numpy.zeros(N)

P_to_W_ROC_table = numpy.zeros((N, 16))

y = 0
for k in [np_l, np_u]:
    for j in [nm_l, nm_u]:
        for i in [Cdo_l, Cdo_u]:
            for l in [e_l, e_u]:
                for h in range(N):

                    k_lift[h] = 1/(math.pi * l * AR) # Drag Due to Lift min

                    L_by_D[h] = 1 /(2*math.sqrt(k_lift[h]*i)) # Min lift to drag ratio


                    Cl_roc[h] = math.sqrt((3*i)/k_lift[h])

                    Vroc[h] = math.sqrt(W_by_S_1[h]*2/(rho_roc*Cl_roc[h]))

                    P_to_W_roc[h] = (1/(thrust*j*k))*((ROC/60)+(Vroc[h]/(0.866*L_by_D[h]*math.sqrt(rho_roc))))

                    P_to_W_ROC_table[h, y] = P_to_W_roc[h]

                y = y+1


# Turns

n = 2 # Load factor
rho_tu = density(100)

Vtu = 18 # Airspeed in m/s

q_tu = Dynamic_Pressure(rho_tu, Vtu)

T_by_W_tu = numpy.zeros(N)
P_to_W_tu = numpy.zeros(N)

P_to_W_Tu_table = numpy.zeros((N, 16))

y = 0
for k in [np_l, np_u]:
    for j in [nm_l, nm_u]:
        for i in [Cdo_l, Cdo_u]:
            for l in [e_l, e_u]:
                for h in range(N):

                    k_lift[h] = 1/(math.pi * l * AR)

                    T_by_W_tu[h] = ((q_tu*i)/W_by_S_1[h])+((n**2)*((k_lift[h]*W_by_S_1[h])/q_tu))

                    P_to_W_tu[h] = (Vtu*T_by_W_tu[h])/(j*k)

                    P_to_W_Tu_table[h, y] = P_to_W_tu[h]

                y = y+1
