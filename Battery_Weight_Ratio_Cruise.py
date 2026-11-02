## Weight analysis model
# Model 25, Battery weight ratio at cruise

def Battery_Weight_Ratio_Cruise(Xc, nm, np, L_by_D_max, K_Battery):

    Wb_by_Wc = Xc/(nm*np*L_by_D_max*K_Battery)*1000

    return Wb_by_Wc
