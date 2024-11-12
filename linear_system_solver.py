import numpy as np


# Calculate the SVD of the coefficient matrix


def solve_system(coefficients):
    U, S, Vh = np.linalg.svd(coefficients)

# Find the null space of the matrix (solutions to Ax = 0)
    null_space = Vh[np.where(S < 0.007)].T  # Adjust the tolerance as needed

    # Generate a non-trivial solution by scaling a vector from the null space
    solution = null_space[:, 0]   # Scale the first vector, adjust the scale as needed

    return solution



# Define the coefficients matrix
coefficients = np.array([
    [0.75, 1, -0.36, -0.48],
    [0.7, 1, -0.329, -0.47],
    [0.65, 1, -0.293, -0.45],
    [0.6, 1, -0.258, -0.43]
])

