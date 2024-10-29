import numpy as np

#x*y*a + x*b + y*c + d - xyz*e - z*x*f - z*g*y - z*h=0
 
def get_coefficients(x, y, z):
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



a = np.array([[0.2, 1],[0.3,1]])
b = np.array([0.32, 0.38])
print(np.linalg.solve(a,b))

