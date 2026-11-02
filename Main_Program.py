### Main Program

import numpy
import matplotlib.pyplot as plt

from K_lift import K_lift
from L_by_D_max import L_by_D_max
from density import density
from Stall_Velocity import Stall_Velocity
from Takeoff_Velocity import Takeoff_Velocity
from Dynamic_Pressure import Dynamic_Pressure
import takeoff, cruise, loiter, turn, Best_cruise

numpy.seterr(divide='ignore', invalid='ignore') # W/S = 0 gives Inf, as in MATLAB

# Initial Values

g = 9.8 # Acceleration due to gravity

# Airplane Models

Cdo = 0.035 #Drag Coefficient
e = 0.8 #Span Efficiency/ Oswald Efficiency
np = 0.6 # Propeller Efficiency
nm = 0.8 # Motor Efficiency
AR = 8 # Aspect Ratio
Payload_wt = 15.5 # Payload weight in N
K_Battery = 60397.0255 # Battery Efficiency
Cl_max = 1.4 # Max Lift Coefficient
Vthrow = 6 # Wind velocity or throw velocity in m/s
Xto = 1 # Takeoff Distance in m

k_lift = K_lift(e, AR) # Drag Due to Lift
L_by_D_max = L_by_D_max(e, AR, Cdo) # Max lift to drag ratio

# Variable that can be changed
We_to_WTo = 0.5 # Empty Weight to Take-Off Weight ratio

# Design point, read off the constraint plot (replaces ginput)
W_by_S = 60 # Wing loading in N/m^2
P_to_W = 10 # Power loading in W/N

# MATLAB globals: share them with the holistic models
for module in (takeoff, cruise, loiter, turn, Best_cruise):
    for name in ('g', 'AR', 'Cdo', 'e', 'np', 'nm', 'Payload_wt', 'We_to_WTo', 'K_Battery', 'Cl_max'):
        setattr(module, name, globals()[name])


def polyxpoly(x1, y1, x2, y2):
    """Intersection points of two polylines (stand-in for MATLAB's polyxpoly)."""
    x1, y1, x2, y2 = (numpy.asarray(v, dtype=float).ravel() for v in (x1, y1, x2, y2))
    p = numpy.stack([x1[:-1], y1[:-1]], 1)[:, None, :]
    r = numpy.stack([numpy.diff(x1), numpy.diff(y1)], 1)[:, None, :]
    q = numpy.stack([x2[:-1], y2[:-1]], 1)[None, :, :]
    s = numpy.stack([numpy.diff(x2), numpy.diff(y2)], 1)[None, :, :]
    cross = lambda a, b: a[..., 0]*b[..., 1] - a[..., 1]*b[..., 0]
    denom = cross(r, s)
    qp = q - p
    t = cross(qp, s)/denom
    u = cross(qp, r)/denom
    hit = (denom != 0) & (t >= 0) & (t <= 1) & (u >= 0) & (u <= 1)
    i, j = numpy.nonzero(hit)
    pts = p[i, 0] + t[i, j][:, None]*r[i, 0]
    pts = numpy.unique(numpy.round(pts, 10), axis=0)
    return pts[:, 0], pts[:, 1]


## Constraint analysis

W_by_S_1 = numpy.arange(0, 250.5, 0.5) # Initial array for constraint analysis

# Take Off

rho_to = density(0) # Altitude in Feet
Vstall = Stall_Velocity(W_by_S_1, rho_to, Cl_max) # Stall velocity model
Vto = Takeoff_Velocity(Vstall)-Vthrow # Take-off velocity model
P_to_W_T = (Vto**3)/(2*g*nm*np*Xto) # Power to weight array used for constraint analysis plot

# Max Speed

rho_ms = density(492.1) # Altitude in Feet
V_ms = 23 # Max Velocity in m/s
q_ms = Dynamic_Pressure(rho_ms, V_ms) # Dynamic Pressure for max speed
T_by_W_ms = (((q_ms*Cdo)/(W_by_S_1)) + ((k_lift * W_by_S_1)/q_ms)) # Thrust to weight required for max speed phase
P_to_W_ms = (V_ms*T_by_W_ms)/(nm*np) # Power to weight array used for constraint analysis plot

# Approach Velocity

rho_app = density(328.1) # Altitude in Feet
Vapp = 9 # Approach velocity in m/s
W_by_S_App = 0.5*rho_app*(Vapp**2)*Cl_max*numpy.ones(len(W_by_S_1))
P_to_W_App = numpy.arange(0, 250.5, 0.5) # Power to weight array used for constraint analysis plot

# Ceiling

rho_ceil = density(6233.6) # Altitude in Feet
Cl = numpy.sqrt((3*Cdo)/k_lift) # Coefficient of lift
Vceil = numpy.sqrt((2*W_by_S_1)/(rho_ceil*Cl)) # Ceiling velocity in m/s
P_to_W_Ceil = (Vceil/(0.886*np*nm*g)) # Power to weight array used for constraint analysis plot

# Rate of Climb

rho_roc = density(1300) # Altitude in Feet
Cl = numpy.sqrt((3*Cdo)/k_lift) # Coefficient of lift
Vroc = numpy.sqrt(W_by_S_1*2/(rho_roc*Cl)) # Rate of climb velocity in m/s
ROC = 100 # Rate of climb in m/min
P_to_W_roc = (1/(nm*np))*((ROC/60)+(Vroc/(0.866*L_by_D_max*numpy.sqrt(rho_roc)))) # Power to weight array used for constraint analysis plot

# Turns

n = 2 # Load factor
rho_tu = density(0) # Altitude in Feet
Vtu = 18 # Turn velocity in m/s
q_tu = Dynamic_Pressure(rho_tu, Vtu) # Dynamic Pressure for turns
T_by_W_tu = ((q_tu*Cdo)/W_by_S_1)+((n**2)*((k_lift*W_by_S_1)/q_tu)) # Thrust to weight required for turns phase
P_to_W_tu = (Vtu*T_by_W_tu)/(nm*np) # Power to weight array used for constraint analysis plot

fig, ax = plt.subplots()

p1, = ax.plot(W_by_S_1, P_to_W_T) # Take off

p2, = ax.plot(W_by_S_1, P_to_W_ms, 'r') # Max Speed
p3, = ax.plot(W_by_S_App, P_to_W_App, 'g') #Approach Velocity
p4, = ax.plot(W_by_S_1, P_to_W_Ceil, 'm') # Ceiling
p5, = ax.plot(W_by_S_1, P_to_W_roc, color=[0.929411764705882, 0.694117647058824,
    0.125490196078431]) # Rate of Climb
p6, = ax.plot(W_by_S_1, P_to_W_tu, 'k') # Turns
ax.legend([p1, p2, p3, p4, p5, p6], ['Take off', 'Max Speed', 'Approach Velocity', 'Ceiling', 'Rate of Climb', 'Turns'])

ax.set_xlabel('Wing loading W/S (N/m^2)')
ax.set_ylabel('Power Loading P/W (Watt/N)')

ax.grid(True)

ax.axis([40, 100, 0, 18])

c1, d1 = polyxpoly(W_by_S_1, P_to_W_T, W_by_S_App, P_to_W_App) # Intersection between take off and approach
c2, d2 = polyxpoly(W_by_S_1, P_to_W_T, W_by_S_1, P_to_W_ms) # Intersection between take off and max speed
c3, d3 = polyxpoly(W_by_S_1, P_to_W_T, W_by_S_1, P_to_W_Ceil) # Intersection between take off and ceiling
c4, d4 = polyxpoly(W_by_S_1, P_to_W_T, W_by_S_1, P_to_W_tu) # Intersection between take off and turns
c5, d5 = polyxpoly(W_by_S_1, P_to_W_T, W_by_S_1, P_to_W_roc) # Intersection between take off and rate of climb

c6, d6 = polyxpoly(W_by_S_1, P_to_W_ms, W_by_S_1, P_to_W_Ceil) # Intersection between max speed and ceiling
c7, d7 = polyxpoly(W_by_S_1, P_to_W_ms, W_by_S_1, P_to_W_tu) # Intersection between max speed and turns
c8, d8 = polyxpoly(W_by_S_1, P_to_W_ms, W_by_S_1, P_to_W_roc) # Intersection between max speed and rate of climb
c9, d9 = polyxpoly(W_by_S_1, P_to_W_ms, W_by_S_App, P_to_W_App) # Intersection between max speed and approach

c10, d10 = polyxpoly(W_by_S_1, P_to_W_Ceil, W_by_S_1, P_to_W_roc) # Intersection between ceiling and rate of climb
c11, d11 = polyxpoly(W_by_S_1, P_to_W_Ceil, W_by_S_1, P_to_W_tu) # Intersection between ceiling and turns
c12, d12 = polyxpoly(W_by_S_1, P_to_W_Ceil, W_by_S_App, P_to_W_App) # Intersection between ceiling and approach

c13, d13 = polyxpoly(W_by_S_1, P_to_W_tu, W_by_S_1, P_to_W_roc) # Intersection between turns and rate of climb
c14, d14 = polyxpoly(W_by_S_1, P_to_W_tu, W_by_S_App, P_to_W_App) # Intersection between turns and approach

c15, d15 = polyxpoly(W_by_S_1, P_to_W_roc, W_by_S_App, P_to_W_App) # Intersection between rate of climb and approach

P1, = ax.plot(c1, d1, 'o', fillstyle='none')
P2, = ax.plot(c2, d2, 'o', fillstyle='none')
P3, = ax.plot(c3, d3, 'o', fillstyle='none')
P4, = ax.plot(c4, d4, 'o', fillstyle='none')
P5, = ax.plot(c5, d5, 'o', fillstyle='none')

P6, = ax.plot(c6, d6, 'o', fillstyle='none')
P7, = ax.plot(c7, d7, 'o', fillstyle='none')
P8, = ax.plot(c8, d8, 'o', fillstyle='none')
P9, = ax.plot(c9, d9, 'o', fillstyle='none')

P10, = ax.plot(c10, d10, 'o', fillstyle='none')
P11, = ax.plot(c11, d11, 'o', fillstyle='none')
P12, = ax.plot(c12, d12, 'o', fillstyle='none')

P13, = ax.plot(c13, d13, 'o', fillstyle='none')
P14, = ax.plot(c14, d14, 'o', fillstyle='none')

P15, = ax.plot(c15, d15, 'o', fillstyle='none')

# ax.legend([P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15],
#     ['Take-off and Approach', 'Take-off and Max speed', 'Take-off and Ceiling',
#     'Take-off and Turns', 'Take-off and Rate of climb', 'Max speed and Ceiling',
#     'Max speed and Turns', 'Max speed and Rate of Climb',
#     'Max speed and Approach', 'Ceiling and Rate of climb', 'Ceiling and Turns',
#     'Ceiling and Apporach', 'Turns and Rate of climb', 'Turns and Approach',
#     'Rate of climb and approach'], fontsize='x-small')

ax.plot(W_by_S, P_to_W, '*') # Design point

## Weight Analysis

# Mission Requirement Model

rho_to = density(0) # Altitude in Feet
rho_c = density(0) # Altitude in Feet
rho_bc = density(0) # Altitude in Feet
rho_l = density(0) # Altitude in Feet
rho_tu = density(0) # Altitude in Feet
Xc = 15 # Cruise distance in KM
Xbc = 15 # Best Range Cruise distance in KM
Vc = 18 # Cruise velocity in m/s
Vl = 11 # Velocity of loiter in m/s
Tl = 0 # Initial Loiter Time in Hours
theta = 34.05 # bank angle in degrees

## Mission Statement Array - Each Input Indexes a Model

# 1 - Takeoff
# 2 - Cruise
# 3 - Loiter
# 4 - Turn
# 5 - Best range cruise

mission = [1, 5, 3, 2, 4] # Depending on the mission statement

## Running Mission Statement
# Initializing Weight Array
Wbs = numpy.zeros(len(mission))

# Looping for Length of Mission Statement
for i in range(len(mission)):
    match mission[i]:
        case 1:
            Wbs[i] = takeoff.takeoff(rho_to, W_by_S, P_to_W)
        case 2:
            Wbs[i] = cruise.cruise(rho_c, Xc, W_by_S, Vc, k_lift)
        case 3:
            Wbs[i] = loiter.loiter(Vl, Tl, rho_l, W_by_S, k_lift)
        case 4:
            Wbs[i] = numpy.real(turn.turn(rho_tu, W_by_S, P_to_W, theta, k_lift))
        case 5:
            Wbs[i] = Best_cruise.Best_cruise(rho_bc, Xbc, W_by_S, k_lift)

## Final Calculation
Wb = sum(Wbs)

Wto = (Payload_wt)/(1-(We_to_WTo+Wb)) # Final Take-off weight

Wempty = We_to_WTo * Wto # Final empty weight

Wbattery = Wto * Wb # Final battery weight

s = Wto/W_by_S # Wing area of the aircraft

b = numpy.sqrt(AR*s) # Wing span of the aircraft

Power = P_to_W * Wto # Final power required to take-off

print('Wbs       =', numpy.array2string(Wbs, precision=5))
print(f'Wb        = {Wb:.4f}')
print(f'Wto       = {Wto:.4f} N')
print(f'Wempty    = {Wempty:.4f} N')
print(f'Wbattery  = {Wbattery:.4f} N')
print(f's         = {s:.4f} m^2')
print(f'b         = {b:.4f} m')
print(f'Power     = {Power:.4f} W')

plt.show()
