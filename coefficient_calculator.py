import numpy as np

 
def get_coefficients_2_way(x, y, z):
    # Coefficients for a, b, c, d, e, f, g, h
    coefficients = [
        x * y,   # coefficient for a
        x,       # coefficient for b
        y,       # coefficient for c
        1,       # coefficient for d
        -x * y * z,  # coefficient for e
        -z * x,  # coefficient for f
        -z * y,  # coefficient for g
        -z       # coefficient for h
    ]
    return coefficients

def get_coefficients_1_way(x, y):
    # Coefficients for a, b, c, d
    coefficients = [
        x,   # coefficient for a
        1,       # coefficient for b
        -x*y,       # coefficient for c
        -y,       # coefficient for d
    ]
    return coefficients


