# region imports
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import numpy as np


# endregion

# region functions
def twoQuadratics(vals, x1, y1, R, a, b):
    """
    f1val and f2val are edited to now accept any number.
    """
    x, y = vals
    # Circle equation: (x - x1)^2 + (y - y1)^2 - R^2 = 0
    f1val = (x - x1) ** 2 + (y - y1) ** 2 - R ** 2
    # Parabola equation: a*x^2 + b - y = 0
    f2val = a * x ** 2 + b - y
    return (f1val, f2val)


def main():
    # Collect inputs with the defaults from the homework
    x1 = float(input("Circle center x1 (default 1): ") or 1.0)
    y1 = float(input("Circle center y1 (default 0): ") or 0.0)
    R = float(input("Circle radius R (default 4): ") or 4.0)
    a = float(input("Parabola width 'a' (default 0.5): ") or 0.5)
    b = float(input("Parabola offset 'b' (default 1.0): ") or 1.0)

    # Find the intersection using fsolve
    # Guessing (2, 2) to find a point in the upper right quadrant
    root = fsolve(twoQuadratics, (2, 2), args=(x1, y1, R, a, b))
    print(f"\nIntersection point found: x = {root[0]:.4f}, y = {root[1]:.4f}")

    # region Plotting
    # Set range from -10 to 10 as required
    xvals = np.linspace(-10, 10, 500)

    # Parabola plotting data
    y_parabola = a * xvals ** 2 + b

    # Circle plotting data (Parametric)
    theta = np.linspace(0, 2 * np.pi, 500)
    x_circle = x1 + R * np.cos(theta)
    y_circle = y1 + R * np.sin(theta)

    plt.figure(figsize=(7, 7))
    plt.plot(xvals, y_parabola, label='Parabola', color='blue')
    plt.plot(x_circle, y_circle, label='Circle', color='red')

    # Mark the intersection point found by fsolve
    plt.plot(root[0], root[1], marker='o', markerfacecolor='none',
             markeredgecolor='green', markersize=12, label='Intersection')

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Problem 2: Circle and Parabola Intersection")
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.show()
    # endregion


if __name__ == "__main__":
    main()