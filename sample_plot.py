import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Coefficients from the given array
coeffs = np.array([-0.12613187, -0.27877737, -0.00631677,  0.02482176, 
                   -0.2995979 , -0.90000701,  0.07472813,  0.01902892])

# Extract coefficients for the function
a, b, c, d, e, f, g, h = coeffs

# Create grid for the 3D plot
x = np.linspace(0, 1, 100)
y = np.linspace(0, 1, 100)
X, Y = np.meshgrid(x, y)

# Calculate Z values based on the rational function formula
Z = (a * X * Y + b * X + c * Y + d) / (e * X * Y + f * X + g * Y + h)

# Create a 3D plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.7)

# Add labels and title
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('f(x, y)')
ax.set_title('3D Surface Plot of Rational Function')

# Show color bar
fig.colorbar(surf, ax=ax)

plt.show()
