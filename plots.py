import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_rational_functions(plots_params, x_range=(0, 1), num_points=10000,points=None):
    x = np.linspace(x_range[0], x_range[1], num_points)
    
    plt.figure(figsize=(8, 6))
    
    # Plot each rational function
    for i, (a, b, c, d) in enumerate(plots_params):
        # Calculate y-values, handling cases where denominator is zero
        y = (a * x + b) / (c * x + d)
        plt.plot(x, y, label=f"Function {i+1}: ({a}*x + {b}) / ({c}*x + {d})")

    if points:
        for (px, py) in points:
            plt.scatter(px, py, color='green', marker='o', label=f"Point ({px}, {py})")
    
    # Set plot labels and legend
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Multiple Rational Functions Plot')
    plt.legend()
    plt.grid(True)
    plt.show()


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_3d_rational_functions(plots_params, x_range=(0, 1), y_range=(0, 1), num_points=100, points=None):
    # Create grid for 3D plot and contour plot
    x = np.linspace(x_range[0], x_range[1], num_points)
    y = np.linspace(y_range[0], y_range[1], num_points)
    X, Y = np.meshgrid(x, y)
    
    # Set up figure and axes
    fig = plt.figure(figsize=(14, 6))
    
    # 3D Plot
    ax1 = fig.add_subplot(121, projection='3d')
    
    # Plot each rational function on the 3D surface
    for i, (a, b, c, d, e, f, g, h) in enumerate(plots_params):
        # Compute Z-values based on the rational function
        Z = (a * X * Y + b * X + c * Y + d) / (e * X * Y + f * X + g * Y + h)
        
        ax1.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.6)
    
    ax1.set_xlabel('X axis')
    ax1.set_ylabel('Y axis')
    ax1.set_zlabel('f(x, y)')
    ax1.set_title('3D Surface Plot of Rational Functions')

    # Contour Plot
    ax2 = fig.add_subplot(122)
    
    # Plot each rational function on the contour plot
    for i, (a, b, c, d, e, f, g, h) in enumerate(plots_params):
        # Compute Z-values for contour plot
        Z = (a * X * Y + b * X + c * Y + d) / (e * X * Y + f * X + g * Y + h)
        
        contour = ax2.contourf(X, Y, Z, 50, cmap='viridis')
    
    ax2.set_xlabel('X axis')
    ax2.set_ylabel('Y axis')
    ax2.set_title('Contour Plot of Rational Functions')
    fig.colorbar(contour, ax=ax2)

    # If points are provided, add them to the plot
    if points:
        for (px, py) in points:
            ax2.scatter(px, py, color='green', marker='o', label=f"Point ({px}, {py})")
    
    # Display plots
    plt.tight_layout()
    plt.show()


    # Contour Plot
    ax2 = fig.add_subplot(122)
    
    # Plot each rational function on the contour plot
    for i, (a, b, c, d) in enumerate(plots_params):
        # Compute Z-values for contour plot
        Z = (a * X + b) / (c * X + d)
        
        contour = ax2.contourf(X, Y, Z, 50, cmap='viridis')
        
    ax2.set_xlabel('X axis')
    ax2.set_ylabel('Y axis')
    ax2.set_title('Contour Plot of Rational Functions')
    fig.colorbar(contour, ax=ax2)

    # If points are provided, add them to the plot
    if points:
        for (px, py) in points:
            ax2.scatter(px, py, color='green', marker='o', label=f"Point ({px}, {py})")
    
    # Display plots
    plt.tight_layout()
    plt.show()


