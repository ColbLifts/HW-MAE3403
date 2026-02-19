#region imports
from math import sqrt, pi, exp
#endregion


#region function definitions

def GPDF(args):
    """
    Gaussian probability density function.
    args = (x, mu, sig)
    """
    x, mu, sig = args
    return (1 / (sig * sqrt(2 * pi))) * exp(-0.5 * ((x - mu) / sig) ** 2)


def Simpson(fn, args, N=100):
    """
    Simpson 1/3 rule integration.
    args = (mu, sig, lhl, rhl)
    """
    mu, sig, lhl, rhl = args

    if N % 2 == 1:
        N += 1

    h = (rhl - lhl) / N

    total = fn((lhl, mu, sig)) + fn((rhl, mu, sig))

    for i in range(1, N):
        x = lhl + i * h
        fx = fn((x, mu, sig))

        if i % 2 == 0:
            total += 2 * fx
        else:
            total += 4 * fx

    return (h / 3) * total


def Probability(PDF, args, c, GT=True):
    """
    Compute probability x<c or x>c for a normal distribution.
    """
    mu, sig = args

    lower = mu - 5 * sig
    upper = c

    prob_less = Simpson(PDF, (mu, sig, lower, upper), N=200)

    if GT:
        return 1 - prob_less
    else:
        return prob_less


def Secant(fcn, x0, x1, maxiter=10, xtol=1e-5):
    """
    Secant method root finder.
    Returns (root, iterations)
    """
    iterations = 0

    while iterations < maxiter:
        f0 = fcn(x0)
        f1 = fcn(x1)

        if f1 - f0 == 0:
            break

        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)

        if abs(x2 - x1) < xtol:
            return x2, iterations + 1

        x0 = x1
        x1 = x2
        iterations += 1

    return x1, iterations


def GaussSeidel(Aaug, x, Niter=15):
    """
    Gauss-Seidel iterative solver.
    Aaug = augmented matrix [A | b]
    x = initial guess vector
    """
    n = len(Aaug)
    ncols = len(Aaug[0])

    for k in range(Niter):
        for i in range(n):

            rhs = Aaug[i][ncols - 1]

            for j in range(n):
                if j != i:
                    rhs -= Aaug[i][j] * x[j]

            x[i] = rhs / Aaug[i][i]

    return x

#endregion
