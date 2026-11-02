## Aircraft model
# Model 7, Take-off Velocity

def Takeoff_Distance(Vto, g, nm, np, P_to_W):

    Xto = ((0.7*Vto)**3)/(g*nm*np*P_to_W)

    return Xto
