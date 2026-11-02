## Weight Analysis model
# Model 29, Battery weight to total weight for Loiter

def Battery_Weight_Ratio_Loiter(Ld, nm, np, L_by_D_l, K_Battery):

    Wb_by_Wl = (Ld/(np*nm*K_Battery*L_by_D_l))*1000

    return Wb_by_Wl
