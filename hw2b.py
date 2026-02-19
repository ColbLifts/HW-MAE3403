from NumericalMethods import Secant
from math import cos


def fn1(x):
    return x - 3 * cos(x)


def fn2(x):
    return x**3 * cos(2 * x)


def main():

    r1 = Secant(fn1, 1, 2, 5, 1e-4)
    r2 = Secant(fn2, 1, 2, 15, 1e-8)
    r3 = Secant(fn2, 1, 2, 3, 1e-8)

    print("root of fn1 = {root:0.6f}, after {iter:0d} iterations".format(root=r1[0], iter=r1[1]))
    print("root of fn2 (15 iter) = {root:0.6f}, after {iter:0d} iterations".format(root=r2[0], iter=r2[1]))
    print("root of fn2 (3 iter) = {root:0.6f}, after {iter:0d} iterations".format(root=r3[0], iter=r3[1]))


if __name__ == "__main__":
    main()
