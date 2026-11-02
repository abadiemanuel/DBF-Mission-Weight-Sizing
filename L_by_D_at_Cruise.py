## Weight analysis model
# Model 24, Lift by drag ratio at cruise

def L_by_D_at_Cruise(W_by_S, Cdo, q, k_lift):

    L_by_D_c = W_by_S/(Cdo*q+(k_lift*((W_by_S)**2)/q))

    return L_by_D_c
