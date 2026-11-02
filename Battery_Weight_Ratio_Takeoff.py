## Weight analysis model
# Model 22, Battery weight ratio for take-off

def Battery_Weight_Ratio_Takeoff(Tto, P_to_W, K_Battery):

    Wb_by_Wto = (Tto*P_to_W)/K_Battery

    return Wb_by_Wto
