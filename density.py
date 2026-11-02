## Enviornmental model
# Model 2, Density model
# Reference: https://www.grc.nasa.gov/WWW/K-12/rocket/atmos.html

def density(h):

    # rho = (101.29*((15.04-0.00649*h+273.1)/288.08)**5.256)/(0.2869*(15.05-0.00649*h+273.1))

    T = 59-0.00356*h # Temp in fahrenheit
    P = 2116*(((T+459.7)/518.6)**5.256) # pressure in lbs/sq ft
    rho = 515.37882*(P/(1718*(T+459.7))) # Deinsity in Slugs/cu-ft converted to kg/m^3

    return rho
