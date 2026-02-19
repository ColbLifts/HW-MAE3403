from copy import deepcopy
from NumericalMethods import GaussSeidel


def make_augmented(A, b):
    Aaug = []
    for i in range(len(A)):
        Aaug.append(A[i] + [b[i]])
    return Aaug


def main():

    # -------- System 1 --------
    A1 = [
        [3, 1, -1],
        [1, 4, 1],
        [2, 1, 2]
    ]
    b1 = [2, 12, 10]

    Aaug1 = make_augmented(A1, b1)
    x_guess1 = [0, 0, 0]

    sol1 = GaussSeidel(deepcopy(Aaug1), x_guess1, 15)

    print("Solution to system 1:")
    print(sol1)

    # -------- System 2 --------
    A2 = [
        [1, 10, 2, 4],
        [3, 1, 4, 12],
        [9, 2, 3, 4],
        [1, 2, 7, 3]
    ]
    b2 = [2, 12, 21, 37]

    Aaug2 = make_augmented(A2, b2)
    x_guess2 = [0, 0, 0, 0]

    sol2 = GaussSeidel(deepcopy(Aaug2), x_guess2, 15)

    print("Solution to system 2:")
    print(sol2)


if __name__ == "__main__":
    main()
