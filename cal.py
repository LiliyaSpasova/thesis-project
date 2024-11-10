import numpy as np
from scipy.linalg import null_space

coefficients = np.array([
    [0.75, 1, -0.36, -0.48],
    [0.7, 1, -0.329, -0.47],
    [0.65, 1, -0.293, -0.45]
])

null_space = null_space(coefficients)

print(null_space)