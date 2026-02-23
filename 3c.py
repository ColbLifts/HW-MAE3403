import math

def is_symmetric(A):
    # Checking if symmetric
    n=len(A)
    for i in range(n):
        for j in range(n):
            if A[i][j] != A[j][i]:
                return False
    return True
def cholesky(A):
    n=len(A)
    L = [[0.0]*n for _ in range(n)]

    for j in range(n):
        sum1 = sum(L[j][s]**2 for s in range(j))
        diag = A[j][j] - sum1
        if diag <= 0:
            raise ValueError("Matrix is not positive")
        L[j][j] = math.sqrt(diag)

        for i in range(j+1, n):
            sum2 = sum(L[i][s]*L[j][s] for s in range(j))
            L[i][j] = (A[i][j] - sum2) / L[j][j]
    return L


def is_positive_definite(A):
    try:
        _ =cholesky(A)
        return True
    except ValueError:
        return False

#Forward and back substitution


def forward_substitution(L, b):
    n = len(L)
    y = [0.0]*n
    for i in range(n):
        sum1 = sum(L[i][j]*y[j] for j in range(i))
        y[i]= (b[i]-sum1) / L[i][i]
    return y


def backward_substitution(U, y):
    n = len(U)
    x = [0.0]*n
    for i in reversed(range(n)):
        sum1 = sum(U[i][j]*x[j] for j in range (i+1, n))
        x[i] = (y[i]-sum1) / U[i][i]
    return x
#Doolittle factorization

# Doolittle LU factorization

def doolittle(A):
    n = len(A)
    L = [[0.0]*n for _ in range(n)]
    U = [[0.0]*n for _ in range(n)]

    for i in range(n):
        L[i][i] = 1.0

    for j in range(n):
        for i in range(j+1):
            sum1 = sum(U[k][j]*L[i][k] for k in range(i))
            U[i][j] = A[i][j] - sum1

        for i in range(j, n):
            sum2 = sum(U[k][j]*L[i][k] for k in range(j))
            L[i][j] = (A[i][j] - sum2) / U[j][j]

    return L, U


# Solve using Cholesky

def solve_cholesky(A, b):
    L = cholesky(A)
    Lt = list(zip(*L))  # transpose
    y = forward_substitution(L, b)
    x = backward_substitution(Lt, y)
    return x


# Solve using Doolittle

def solve_doolittle(A, b):
    L, U = doolittle(A)
    y = forward_substitution(L, b)
    x = backward_substitution(U, y)
    return x

# Main program

def main():
    print("=== HW3c: Matrix Solver ===")

    # System 1

    A1 = [
        [1, -1, 3, 2],
        [-1, 5, -5, -2],
        [3, -5, 19, 3],
        [2, -2, 3, 21]
    ]
    b1 = [15, -35, 94, 1]

    print("\nSystem 1:")
    if is_symmetric(A1) and is_positive_definite(A1):
        print("Method used: Cholesky")
        x1 = solve_cholesky(A1, b1)
    else:
        print("Method used: Doolittle")
        x1 = solve_doolittle(A1, b1)

    for i, val in enumerate(x1, start=1):
        print(f"x{i} = {val:.6f}")


    # System 2

    A2 = [
        [4, 2, 4, 0],
        [2, 2, 3, 2],
        [4, 3, 6, 3],
        [0, 2, 3, 9]
    ]
    b2 = [20, 36, 60, 122]

    print("\nSystem 2:")
    if is_symmetric(A2) and is_positive_definite(A2):
        print("Method used: Cholesky")
        x2 = solve_cholesky(A2, b2)
    else:
        print("Method used: Doolittle")
        x2 = solve_doolittle(A2, b2)

    for i, val in enumerate(x2, start=1):
        print(f"x{i} = {val:.6f}")

if __name__ == "__main__":
    main()
