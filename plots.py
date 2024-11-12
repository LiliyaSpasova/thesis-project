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


coeff_1=[0.993,0.001,1,0.786]
coeff_2=[-0.426290445,-0.168517666,-0.190759412,-0.868037499]

coeff_list=[coeff_1,coeff_2]
#plot_rational_functions(coeff_list)