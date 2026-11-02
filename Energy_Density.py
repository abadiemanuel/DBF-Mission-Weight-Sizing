## Battery model
# Model 20, Battery energy density

def Energy_Density(Volt, mAh, wt):

    K_Battery = ((Volt*mAh)*3600)/(wt*0.0098) # Battery Energy density in J/N

    return K_Battery
