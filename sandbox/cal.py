import numpy as np
from scipy.optimize import minimize
from scipy import linalg

# Coefficients for the equations
coefficients = np.array([
    [0.75, 1, -0.36, -0.48],
    [0.7, 1, -0.329, -0.47],
    [0.65, 1, -0.293, -0.45],
    [0.6, 1, -0.258, -0.43]
])


for (a,b,c,d) in coefficients:
     print  (a*-4.2629044 - 1.68517666 + c* -1.90759412 + d* -8.68037499)

print(linalg.det(coefficients))

# Example 1: Least Squares Solution
# Use np.linalg.lstsq to get the least squares solution
print(np.linalg.lstsq(coefficients,np.zeros(4)))
# Example 2: Check for approximate solution within a tolerance
tolerance = 0.0001  # You can adjust this tolerance value
# Use SVD to compute the pseudo-inverse of the matrix
U, S, Vt = np.linalg.svd(coefficients)

# Compute the pseudo-inverse (using the thresholding on singular values for better numerical stability)
S_inv = np.diag(1 / S)  # Inverse of non-zero singular values
pseudo_inverse = Vt.T @ S_inv @ U.T

print('Pseudo-inverse: ', pseudo_inverse)

# Find the solution close to the zero vector (allowing margin of error)
solution = pseudo_inverse @ np.zeros(coefficients.shape[0])

print('Solution', solution)

# Check if the result of A @ solution is within the tolerance
check_result_svd = np.dot(coefficients, solution)
approximate_solution_valid_svd = np.all(np.abs(check_result_svd) < tolerance)

print(solution, check_result_svd, approximate_solution_valid_svd)


import numpy as np

# Define the coefficients matrix
coefficients = np.array([
    [0.75, 1, -0.36, -0.48],
    [0.7, 1, -0.329, -0.47],
    [0.65, 1, -0.293, -0.45],
    [0.6, 1, -0.258, -0.43]
])

# Calculate the SVD of the coefficient matrix
U, S, Vh = np.linalg.svd(coefficients)

# Find the null space of the matrix (solutions to Ax = 0)
null_space = Vh[np.where(S < 0.007)].T  # Adjust the tolerance as needed

# Generate a non-trivial solution by scaling a vector from the null space
solution = null_space[:, 0]   # Scale the first vector, adjust the scale as needed

print("Non-trivial solution:", solution)
