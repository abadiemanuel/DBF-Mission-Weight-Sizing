## Weight analysis model
# Model 21, Take-off time

def Takeoff_Time(Vto, g, nm, np, P_to_W):

    Tto = (0.5*(Vto)**2)/(g*P_to_W*np*nm)

    return Tto
